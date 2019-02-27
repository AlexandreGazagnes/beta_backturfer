-- JOIN REQUEST

-- pturf
USE pturf;

-- clear namespaces
DROP TABLE IF EXISTS temp_cachedate;
DROP TABLE IF EXISTS temp_caractrap;

-- create temp_cachedate
CREATE TABLE temp_cachedate (
    id bigint(11) NOT NULL,
    comp int(11) NOT NULL,
    jour date NOT NULL,
    hippo tinytext NOT NULL,
    numcourse bigint(11) NOT NULL,
    cl tinytext NOT NULL,
    dist smallint(4) NOT NULL,
    partant int(11) NOT NULL,
    typec text NOT NULL,
    cheque text NOT NULL,
    numero decimal(2,0) NOT NULL,
    cheval text NOT NULL,
    sexe text NOT NULL,
    age int(11) NOT NULL,
    cotedirect decimal(5,2) NOT NULL,
    coteprob decimal(5,2) NOT NULL
                                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- copy new tab
INSERT INTO temp_cachedate 
SELECT id, comp, jour, hippo, numcourse, cl, dist,  partant, typec, cheque, numero, cheval, sexe, age, cotedirect, coteprob 
FROM cachedate WHERE jour > "2016-01-01" ;


-- create temp_caractrap
CREATE TABLE temp_caractrap (
  id bigint(11) NOT NULL,
  comp int(11) NOT NULL,
  heure time ,
  reun varchar(255) ,
  prix double ,
  prixnom varchar(255) ,
  partant varchar(255) ,
  dist smallint(4),
  quinte double ,
  arriv varchar(255) ,
  url text
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- copy new tab
INSERT INTO temp_caractrap 
SELECT id, comp, heure, reun, prix, prixnom, partant, dist, quinte, arriv, url 
FROM caractrap WHERE jour > "2016-01-01" ;



/*-- create temp_merge
CREATE TABLE temp_merge (
    id bigint(11) NOT NULL,
    comp int(11) NOT NULL,
    jour date NOT NULL,
    hippo tinytext NOT NULL,
    numcourse bigint(11) NOT NULL,
    cl tinytext NOT NULL,
    dist smallint(4) NOT NULL,
    partant int(11) NOT NULL,
    typec text NOT NULL,
    cheque text NOT NULL,
    numero decimal(2,0) NOT NULL,
    cheval text NOT NULL,
    sexe text NOT NULL,
    age int(11) NOT NULL,
    cotedirect decimal(5,2) NOT NULL,
    coteprob decimal(5,2) NOT NULL,
    id bigint(11) NOT NULL,
    comp int(11) NOT NULL,
    heure time ,
    reun varchar(255) DEFAULT NULL,
    prix double DEFAULT NULL,
    prixnom varchar(255) DEFAULT NULL,
    partant varchar(255) DEFAULT NULL,
    quinte double DEFAULT NULL,
    arriv varchar(255) DEFAULT NULL,
    url text NOT NULL
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO temp_merge
SELECT  * 
FROM temp_cachedate LEFT JOIN temp_caractrap on temp_cachedate.comp = temp_caractrap.comp ; */

SELECT * FROM temp_cachedate LEFT JOIN temp_caractrap ON temp_cachedate.comp = temp_caractrap.comp ; 


