from __future__ import annotations

from typing import TYPE_CHECKING

import ibis.common.exceptions as com
import ibis.expr.operations as ops
from ibis.backends.base.sql.registry import (
    aggregate,
    fixed_arity,
    helpers,
    quote_identifier,
    unary,
)
from ibis.backends.base.sql.registry import (
    operation_registry as base_operation_registry,
)
from ibis.backends.base.sql.registry.main import varargs
from ibis.common.temporal import TimestampUnit

if TYPE_CHECKING:
    from ibis.backends.base.sql.compiler import ExprTranslator

operation_registry = base_operation_registry.copy()


def type_to_sql_string(tval):
    if tval.is_array():
        return f"array<{helpers.type_to_sql_string(tval.value_type)}>"
    return helpers.type_to_sql_string(tval)


def _not(translator: ExprTranslator, op: ops.Node) -> str:
    formatted_arg = translator.translate(op.arg)
    if helpers.needs_parens(op.arg):
        formatted_arg = helpers.parenthesize(formatted_arg)
    return f"NOT CAST({formatted_arg} AS boolean)"


def _count_star(translator: ExprTranslator, op: ops.Node) -> str:
    if (where := op.where) is not None:
        condition = f" FILTER (WHERE {translator.translate(where)})"
    else:
        condition = ""

    return f"COUNT(*){condition}"


def _string_concat(translator: ExprTranslator, op: ops.StringConcat) -> str:
    joined_args = ", ".join(map(translator.translate, op.arg))
    return f"CONCAT({joined_args})"


def _strftime(translator: ExprTranslator, op: ops.Strftime) -> str:
    import sqlglot as sg

    import ibis.expr.datatypes as dt

    hive_dialect = sg.dialects.hive.Hive
    if (time_mapping := getattr(hive_dialect, "TIME_MAPPING", None)) is None:
        time_mapping = hive_dialect.time_mapping
    reverse_hive_mapping = {v: k for k, v in time_mapping.items()}

    format_str = translator.translate(op.format_str)
    transformed_format_str = sg.time.format_time(format_str, reverse_hive_mapping)
    arg = translator.translate(ops.Cast(op.arg, to=dt.string))

    return f"FROM_UNIXTIME(UNIX_TIMESTAMP({arg}), {transformed_format_str})"


def _date(translator: ExprTranslator, op: ops.Node) -> str:
    (arg,) = op.args
    return f"CAST({translator.translate(arg)} AS DATE)"


def _extract_field(sql_attr: str) -> str:
    def extract_field_formatter(translator: ExprTranslator, op: ops.Node) -> str:
        arg = translator.translate(op.args[0])
        return f"EXTRACT({sql_attr} from {arg})"

    return extract_field_formatter


def _cast(translator: ExprTranslator, op: ops.generic.Cast) -> str:
    arg, to = op.arg, op.to
    arg_translated = translator.translate(arg)
    if to.is_timestamp():
        if arg.dtype.is_numeric():
            arg_translated = f"FROM_UNIXTIME({arg_translated})"

        if to.timezone:
            return f"TO_TIMESTAMP(CONVERT_TZ(CAST({arg_translated} AS STRING), 'UTC+0', '{to.timezone}'))"
        else:
            return f"TO_TIMESTAMP({arg_translated}, 'yyyy-MM-dd HH:mm:ss.SSS')"

    elif to.is_date():
        return f"CAST({arg_translated} AS date)"
    elif to.is_json():
        return arg_translated
    elif op.arg.dtype.is_temporal() and op.to.is_int64():
        return f"1000000 * unix_timestamp({arg_translated})"
    else:
        sql_type = type_to_sql_string(op.to)
        return f"CAST({arg_translated} AS {sql_type})"


def _left_op_right(translator: ExprTranslator, op_node: ops.Node, op_sign: str) -> str:
    """Utility to be used in operators that perform '{op.left} {op_sign} {op.right}'."""
    return f"{translator.translate(op_node.left)} {op_sign} {translator.translate(op_node.right)}"


def _interval_add(translator: ExprTranslator, op: ops.temporal.IntervalSubtract) -> str:
    return _left_op_right(translator=translator, op_node=op, op_sign="+")


def _interval_subtract(
    translator: ExprTranslator, op: ops.temporal.IntervalSubtract
) -> str:
    return _left_op_right(translator=translator, op_node=op, op_sign="-")


def _literal(translator: ExprTranslator, op: ops.Literal) -> str:
    from ibis.backends.flink.utils import translate_literal

    return translate_literal(op)


def _try_cast(translator: ExprTranslator, op: ops.Node) -> str:
    arg_formatted = translator.translate(op.arg)

    if op.arg.dtype.is_temporal() and op.to.is_numeric():
        # The cast from TIMESTAMP type to NUMERIC type is not allowed.
        # It's recommended to use UNIX_TIMESTAMP(CAST(timestamp_col AS STRING)) instead.
        return f"UNIX_TIMESTAMP(TRY_CAST({arg_formatted} AS STRING))"
    else:
        sql_type = type_to_sql_string(op.to)
        return f"TRY_CAST({arg_formatted} AS {sql_type})"


def _filter(translator: ExprTranslator, op: ops.Node) -> str:
    bool_expr = translator.translate(op.bool_expr)
    true_expr = translator.translate(op.true_expr)
    false_null_expr = translator.translate(op.false_null_expr)

    # [TODO](chloeh13q): It's preferable to use the FILTER syntax instead of CASE WHEN
    # to let the planner do more optimizations to reduce the state size; besides, FILTER
    # is more compliant with the SQL standard.
    # For example,
    # ```
    # COUNT(DISTINCT CASE WHEN flag = 'app' THEN user_id ELSE NULL END) AS app_uv
    # ```
    # is equivalent to
    # ```
    # COUNT(DISTINCT) FILTER (WHERE flag = 'app') AS app_uv
    # ```
    return f"CASE WHEN {bool_expr} THEN {true_expr} ELSE {false_null_expr} END"


def _format_window_start(translator: ExprTranslator, boundary):
    if boundary is None:
        return "UNBOUNDED PRECEDING"

    if isinstance(boundary.value, ops.Literal) and boundary.value.value == 0:
        return "CURRENT ROW"

    value = translator.translate(boundary.value)
    return f"{value} PRECEDING"


def _format_window_end(translator: ExprTranslator, boundary):
    if boundary is None:
        raise com.UnsupportedOperationError(
            "OVER RANGE FOLLOWING windows are not supported in Flink yet"
        )

    value = boundary.value
    if isinstance(value, ops.Cast):
        value = boundary.value.arg
    if isinstance(value, ops.Literal):
        if value.value != 0:
            raise com.UnsupportedOperationError(
                "OVER RANGE FOLLOWING windows are not supported in Flink yet"
            )

    return "CURRENT ROW"


def _format_window_frame(translator: ExprTranslator, func, frame):
    components = []

    if frame.group_by:
        partition_args = ", ".join(map(translator.translate, frame.group_by))
        components.append(f"PARTITION BY {partition_args}")

    (order_by,) = frame.order_by
    components.append(f"ORDER BY {translator.translate(order_by)}")

    if frame.start is None and frame.end is None:
        # no-op, default is full sample
        pass
    elif not isinstance(func, translator._forbids_frame_clause):
        # [NOTE] Flink allows
        # "ROWS BETWEEN INTERVAL [...] PRECEDING AND CURRENT ROW"
        # but not
        # "RANGE BETWEEN [...] PRECEDING AND CURRENT ROW",
        # but `.over(rows=(-ibis.interval(...), 0)` is not allowed in Ibis
        if isinstance(frame, ops.RangeWindowFrame):
            if not frame.start.value.dtype.is_interval():
                # [TODO] need to expand support for range-based interval windowing on expr
                # side, for now only ibis intervals can be used
                raise com.UnsupportedOperationError(
                    "Data Type mismatch between ORDER BY and RANGE clause"
                )

        start = _format_window_start(translator, frame.start)
        end = _format_window_end(translator, frame.end)

        frame = f"{frame.how.upper()} BETWEEN {start} AND {end}"
        components.append(frame)

    return "OVER ({})".format(" ".join(components))


def _window(translator: ExprTranslator, op: ops.Node) -> str:
    frame = op.frame
    if not frame.order_by:
        raise com.UnsupportedOperationError(
            "Flink engine does not support generic window clause with no order by"
        )
    if len(frame.order_by) > 1:
        raise com.UnsupportedOperationError(
            "Windows in Flink can only be ordered by a single time column"
        )

    _unsupported_reductions = translator._unsupported_reductions

    func = op.func.__window_op__

    if isinstance(func, _unsupported_reductions):
        raise com.UnsupportedOperationError(
            f"{type(func)} is not supported in window functions"
        )

    if isinstance(frame, ops.RowsWindowFrame):
        if frame.max_lookback is not None:
            raise NotImplementedError(
                "Rows with max lookback is not implemented for SQL-based backends."
            )

    window_formatted = _format_window_frame(translator, func, frame)

    arg_formatted = translator.translate(func.__window_op__)
    result = f"{arg_formatted} {window_formatted}"

    if isinstance(func, (ops.RankBase, ops.NTile)):
        return f"({result} - 1)"
    return result


def _clip(translator: ExprTranslator, op: ops.Node) -> str:
    from ibis.backends.flink.datatypes import FlinkType

    arg = translator.translate(op.arg)

    if op.upper is not None:
        upper = translator.translate(op.upper)
        arg = f"IF({arg} > {upper} AND {arg} IS NOT NULL, {upper}, {arg})"

    if op.lower is not None:
        lower = translator.translate(op.lower)
        arg = f"IF({arg} < {lower} AND {arg} IS NOT NULL, {lower}, {arg})"

    return f"CAST({arg} AS {FlinkType.from_ibis(op.dtype)!s})"


def _ntile(translator: ExprTranslator, op: ops.NTile) -> str:
    return f"NTILE({op.buckets.value})"


def _floor_divide(translator: ExprTranslator, op: ops.Node) -> str:
    left = translator.translate(op.left)
    right = translator.translate(op.right)
    return f"FLOOR(({left}) / ({right}))"


def _array(translator: ExprTranslator, op: ops.Array) -> str:
    return f"ARRAY[{', '.join(map(translator.translate, op.exprs))}]"


def _array_index(translator: ExprTranslator, op: ops.ArrayIndex):
    table_column = op.arg
    index = op.index

    table_column_translated = translator.translate(table_column)
    index_translated = translator.translate(index)

    return f"{table_column_translated} [ {index_translated} + 1 ]"


def _array_length(translator: ExprTranslator, op: ops.ArrayLength) -> str:
    return f"CARDINALITY({translator.translate(op.arg)})"


def _array_position(translator: ExprTranslator, op: ops.ArrayPosition) -> str:
    arg = translator.translate(op.arg)
    other = translator.translate(op.other)
    return f"ARRAY_POSITION({arg}, {other}) - 1"


def _array_slice(translator: ExprTranslator, op: ops.ArraySlice) -> str:
    array = translator.translate(op.arg)
    start = op.start.value
    # The offsets are 1-based for ARRAY_SLICE.
    # Ref: https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/functions/systemfunctions
    if start >= 0:
        start += 1

    if op.stop is None:
        return f"ARRAY_SLICE({array}, {start})"

    stop = op.stop.value
    if stop >= 0:
        return f"ARRAY_SLICE({array}, {start}, {stop})"
    else:
        # To imitate the behavior of pandas array slicing.
        return f"ARRAY_SLICE({array}, {start}, CARDINALITY({array}) - {abs(stop)})"


def _json_get_item(translator: ExprTranslator, op: ops.json.JSONGetItem) -> str:
    arg_translated = translator.translate(op.arg)
    if op.index.dtype.is_integer():
        query_path = f"$[{op.index.value}]"
    else:  # is string
        query_path = f"$.{op.index.value}"

    return (
        f"JSON_QUERY({arg_translated}, '{query_path}' WITH CONDITIONAL ARRAY WRAPPER)"
    )


def _map(translator: ExprTranslator, op: ops.maps.Map) -> str:
    key_array = translator.translate(op.keys)
    value_array = translator.translate(op.values)

    return f"MAP_FROM_ARRAYS({key_array}, {value_array})"


def _map_get(translator: ExprTranslator, op: ops.maps.MapGet) -> str:
    map_ = translator.translate(op.arg)
    key = translator.translate(op.key)
    return f"{map_} [ {key} ]"


def _struct_field(translator: ExprTranslator, op: ops.StructField) -> str:
    arg = translator.translate(op.arg)
    return f"{arg}.`{op.field}`"


def _day_of_week_index(
    translator: ExprTranslator, op: ops.temporal.DayOfWeekIndex
) -> str:
    arg = translator.translate(op.arg)
    return f"MOD(DAYOFWEEK({arg}) + 5, 7)"


def _day_of_week_name(
    translator: ExprTranslator, op: ops.temporal.DayOfWeekName
) -> str:
    arg = translator.translate(op.arg)
    map_str = "1=Sunday,2=Monday,3=Tuesday,4=Wednesday,5=Thursday,6=Friday,7=Saturday"
    return f"STR_TO_MAP('{map_str}')[CAST(DAYOFWEEK(CAST({arg} AS DATE)) AS STRING)]"


def _date_add(translator: ExprTranslator, op: ops.temporal.DateAdd) -> str:
    return _left_op_right(translator=translator, op_node=op, op_sign="+")


def _date_delta(translator: ExprTranslator, op: ops.temporal.DateDelta) -> str:
    left = translator.translate(op.left)
    right = translator.translate(op.right)
    unit = op.part.value.upper()

    return (
        f"TIMESTAMPDIFF({unit}, CAST({right} AS TIMESTAMP), CAST({left} AS TIMESTAMP))"
    )


def _date_diff(translator: ExprTranslator, op: ops.temporal.DateDiff) -> str:
    raise com.UnsupportedOperationError("DATE_DIFF is not supported in Flink.")


def _date_from_ymd(translator: ExprTranslator, op: ops.temporal.DateFromYMD) -> str:
    year, month, day = (
        f"CAST({translator.translate(e)} AS STRING)"
        for e in [op.year, op.month, op.day]
    )
    concat_string = f"CONCAT({year}, '-', {month}, '-', {day})"
    return f"CAST({concat_string} AS DATE)"


def _date_sub(translator: ExprTranslator, op: ops.temporal.DateSub) -> str:
    return _left_op_right(translator=translator, op_node=op, op_sign="-")


def _extract_epoch_seconds(translator: ExprTranslator, op: ops.Node) -> str:
    arg = translator.translate(op.arg)
    return f"UNIX_TIMESTAMP(CAST({arg} AS STRING))"


def _string_to_timestamp(
    translator: ExprTranslator, op: ops.temporal.StringToTimestamp
) -> str:
    arg = translator.translate(op.arg)
    format_string = translator.translate(op.format_str)
    return f"TO_TIMESTAMP({arg}, {format_string})"


def _time(translator: ExprTranslator, op: ops.temporal.Time) -> str:
    if op.arg.dtype.is_timestamp():
        datetime = op.arg.value
        return f"TIME '{datetime.hour}:{datetime.minute}:{datetime.second}.{datetime.microsecond}'"

    else:
        raise com.UnsupportedOperationError(f"Does NOT support dtype= {op.arg.dtype}")


def _time_delta(translator: ExprTranslator, op: ops.temporal.TimeDiff) -> str:
    left = translator.translate(op.left)
    right = translator.translate(op.right)
    unit = op.part.value.upper()

    return (
        f"TIMESTAMPDIFF({unit}, CAST({right} AS TIMESTAMP), CAST({left} AS TIMESTAMP))"
    )


def _time_from_hms(translator: ExprTranslator, op: ops.temporal.TimeFromHMS) -> str:
    hours, minutes, seconds = (
        f"CAST({translator.translate(e)} AS STRING)"
        for e in [op.hours, op.minutes, op.seconds]
    )
    concat_string = f"CONCAT({hours}, ':', {minutes}, ':', {seconds})"
    return f"CAST({concat_string} AS TIME)"


def _timestamp_add(translator: ExprTranslator, op: ops.temporal.TimestampAdd) -> str:
    return _left_op_right(translator=translator, op_node=op, op_sign="+")


def _timestamp_bucket(
    translator: ExprTranslator, op: ops.temporal.TimestampBucket
) -> str:
    arg_translated = translator.translate(op.arg)

    unit = op.interval.dtype.unit.name
    unit_for_mod = "DAYOFMONTH" if unit == "DAY" else unit
    bucket_width = op.interval.value
    offset = op.offset.value if op.offset else 0

    arg_offset = f"TIMESTAMPADD({unit}, -({offset}), {arg_translated})"
    num = f"{unit_for_mod}({arg_offset})"
    mod = f"{num} % {bucket_width}"

    return f"TIMESTAMPADD({unit}, -({mod}) + {offset}, FLOOR({arg_offset} TO {unit}))"


def _timestamp_delta(
    translator: ExprTranslator, op: ops.temporal.TimestampDelta
) -> str:
    left = translator.translate(op.left)
    right = translator.translate(op.right)
    unit = op.part.value.upper()

    return f"TIMESTAMPDIFF({unit}, {right}, {left})"


def _timestamp_diff(translator: ExprTranslator, op: ops.temporal.TimestampDiff) -> str:
    return _left_op_right(translator=translator, op_node=op, op_sign="-")


def _timestamp_sub(translator: ExprTranslator, op: ops.temporal.TimestampSub) -> str:
    table_column = op.left
    interval = op.right

    table_column_translated = translator.translate(table_column)
    interval_translated = translator.translate(interval)
    return f"{table_column_translated} - {interval_translated}"


def _timestamp_from_unix(translator: ExprTranslator, op: ops.TimestampFromUNIX) -> str:
    arg, unit = op.arg, op.unit

    if unit == TimestampUnit.MILLISECOND:
        precision = 3
    elif unit == TimestampUnit.SECOND:
        precision = 0
    else:
        raise ValueError(f"{unit!r} unit is not supported!")

    arg = translator.translate(op.arg)
    return f"CAST(TO_TIMESTAMP_LTZ({arg}, {precision}) AS TIMESTAMP)"


def _timestamp_from_ymdhms(
    translator: ExprTranslator, op: ops.temporal.TimestampFromYMDHMS
) -> str:
    year, month, day, hours, minutes, seconds = (
        f"CAST({translator.translate(e)} AS STRING)"
        for e in [op.year, op.month, op.day, op.hours, op.minutes, op.seconds]
    )
    concat_string = f"CONCAT({year}, '-', {month}, '-', {day}, ' ', {hours}, ':', {minutes}, ':', {seconds})"
    return f"CAST({concat_string} AS TIMESTAMP)"


def _struct_field(translator, op):
    arg = translator.translate(op.arg)
    return f"{arg}.{quote_identifier(op.field, force=True)}"


operation_registry.update(
    {
        # Unary operations
        ops.Not: _not,
        ops.NullIf: fixed_arity("nullif", 2),
        ops.RandomScalar: lambda *_: "rand()",
        ops.Degrees: unary("degrees"),
        ops.Radians: unary("radians"),
        # Unary aggregates
        ops.ApproxCountDistinct: aggregate.reduction("approx_count_distinct"),
        ops.CountStar: _count_star,
        # String operations
        ops.RegexSearch: fixed_arity("regexp", 2),
        ops.StringConcat: _string_concat,
        ops.Strftime: _strftime,
        ops.StringLength: unary("char_length"),
        ops.StrRight: fixed_arity("right", 2),
        # Timestamp operations
        ops.Date: _date,
        ops.ExtractEpochSeconds: _extract_epoch_seconds,
        ops.ExtractYear: _extract_field("year"),  # equivalent to YEAR(date)
        ops.ExtractMonth: _extract_field("month"),  # equivalent to MONTH(date)
        ops.ExtractDay: _extract_field("day"),  # equivalent to DAYOFMONTH(date)
        ops.ExtractQuarter: _extract_field("quarter"),  # equivalent to QUARTER(date)
        ops.ExtractWeekOfYear: _extract_field("week"),  # equivalent to WEEK(date)
        ops.ExtractDayOfYear: _extract_field("doy"),  # equivalent to DAYOFYEAR(date)
        ops.ExtractHour: _extract_field("hour"),  # equivalent to HOUR(timestamp)
        ops.ExtractMinute: _extract_field("minute"),  # equivalent to MINUTE(timestamp)
        ops.ExtractSecond: _extract_field("second"),  # equivalent to SECOND(timestamp)
        ops.ExtractMillisecond: _extract_field("millisecond"),
        ops.ExtractMicrosecond: _extract_field("microsecond"),
        # Other operations
        ops.Cast: _cast,
        ops.Coalesce: varargs("coalesce"),
        ops.IntervalAdd: _interval_add,
        ops.IntervalSubtract: _interval_subtract,
        ops.Literal: _literal,
        ops.TryCast: _try_cast,
        ops.IfElse: _filter,
        ops.Window: _window,
        ops.Clip: _clip,
        ops.NTile: _ntile,
        # Binary operations
        ops.Power: fixed_arity("power", 2),
        ops.FloorDivide: _floor_divide,
        # Collection operations
        ops.Array: _array,
        ops.ArrayContains: fixed_arity("ARRAY_CONTAINS", 2),
        ops.ArrayDistinct: fixed_arity("ARRAY_DISTINCT", 1),
        ops.ArrayIndex: _array_index,
        ops.ArrayLength: _array_length,
        ops.ArrayPosition: _array_position,
        ops.ArrayRemove: fixed_arity("ARRAY_REMOVE", 2),
        ops.ArraySlice: _array_slice,
        ops.ArrayUnion: fixed_arity("ARRAY_UNION", 2),
        ops.JSONGetItem: _json_get_item,
        ops.Map: _map,
        ops.MapGet: _map_get,
        ops.StructField: _struct_field,
        # Temporal functions
        ops.DateAdd: _date_add,
        ops.DateDelta: _date_delta,
        ops.DateDiff: _date_diff,
        ops.DateFromYMD: _date_from_ymd,
        ops.DateSub: _date_sub,
        ops.DayOfWeekIndex: _day_of_week_index,
        ops.DayOfWeekName: _day_of_week_name,
        ops.StringToTimestamp: _string_to_timestamp,
        ops.Time: _time,
        ops.TimeDelta: _time_delta,
        ops.TimeFromHMS: _time_from_hms,
        ops.TimestampAdd: _timestamp_add,
        ops.TimestampBucket: _timestamp_bucket,
        ops.TimestampDelta: _timestamp_delta,
        ops.TimestampDiff: _timestamp_diff,
        ops.TimestampFromUNIX: _timestamp_from_unix,
        ops.TimestampFromYMDHMS: _timestamp_from_ymdhms,
        ops.TimestampSub: _timestamp_sub,
        ops.StructField: _struct_field,
    }
)

_invalid_operations = {
    # ibis.expr.operations.numeric
    ops.IsNan,
    ops.IsInf,
    # ibis.expr.operations.reductions
    ops.ApproxMedian,
    # ibis.expr.operations.strings
    ops.Translate,
    ops.FindInSet,
}

operation_registry = {
    k: v for k, v in operation_registry.items() if k not in _invalid_operations
}
