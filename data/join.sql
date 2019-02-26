

-- create 2 new tabs
CREATE TABLE temp_cachedate LIKE cachedate;
CREATE TABLE temp_caractrap LIKE caractrap;



-- copy new tabs
INSERT INTO temp_cachedate 
SELECT id, comp, jour, hippo, numcourse, cl, dist,	partant, typec, cheque,	numero,	cheval,	sexe, age, cotedirect, coteprob 
FROM cachedate WHERE jour > "2016-01-01" ;



INSERT INTO temp_caractrap SELECT * FROM caractrap WHERE jour > "2016-01-01" ;

SELECT * FROM temp_cachedate LEFT JOIN temp_caractrap ON temp_cachedate.comp = temp_caractrap.comp ; 



DROP TABLE temp_cachedate; 
DROP TABLE temp_caractrap; 

