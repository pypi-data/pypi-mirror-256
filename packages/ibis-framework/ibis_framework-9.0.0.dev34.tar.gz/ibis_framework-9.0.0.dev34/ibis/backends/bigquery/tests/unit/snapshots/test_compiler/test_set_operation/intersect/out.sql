SELECT
  t0.`a`
FROM (
  SELECT
    t1.*
  FROM t0 AS t1
  INTERSECT DISTINCT
  SELECT
    t1.*
  FROM t1
) AS t0