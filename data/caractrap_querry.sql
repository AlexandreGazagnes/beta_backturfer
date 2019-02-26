ALTER TABLE caractrap CHARACTER SET = utf8;


SELECT *  
FROM caractrap 
WHERE jour > "2018-01-01" 
INTO OUTFILE '/var/lib/mysql-files/caractrap_2018.csv' 
FIELDS TERMINATED 
BY '???' 
LINES TERMINATED BY '!!!';



