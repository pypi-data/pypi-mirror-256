ALTER TABLE tbl PARTITION (year=2007, month=4)
SET SERDEPROPERTIES (
  'baz'='3'
)