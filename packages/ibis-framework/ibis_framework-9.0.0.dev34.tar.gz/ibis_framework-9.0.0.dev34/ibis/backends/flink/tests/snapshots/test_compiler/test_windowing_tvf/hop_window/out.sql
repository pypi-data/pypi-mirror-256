SELECT t0.*
FROM TABLE(HOP(TABLE `table`, DESCRIPTOR(`i`), INTERVAL '1' MINUTE, INTERVAL '15' MINUTE)) t0