SELECT sum(t0.`d`) OVER (ORDER BY t0.`f` ASC ROWS BETWEEN 5 PRECEDING AND UNBOUNDED FOLLOWING) AS `foo`
FROM `alltypes` t0