SELECT * 
FROM cachedate 
WHERE jour > "2018-01-01" 
INTO OUTFILE '/var/lib/mysql-files/cachedate_2018.csv' 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';