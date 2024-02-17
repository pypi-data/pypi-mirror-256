SELECT sum(t0.`f`) OVER (ORDER BY t0.`f` ASC RANGE BETWEEN INTERVAL '00 08:20:00.000000' DAY TO SECOND PRECEDING AND CURRENT ROW) AS `Sum(f)`
FROM table t0