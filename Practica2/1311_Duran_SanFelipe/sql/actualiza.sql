--ADRIAN SAN FELIPE Y LUIS MIGUEL DURAN, GRUPO 1311, SISTEMAS INFORMATICOS I
-- Creamos la tabla alertas que usará el updInventory.sql
DROP TABLE IF EXISTS alertas;
CREATE TABLE alertas(
  prod_id INTEGER NOT NULL
);

--SECUENCIA PARA ID DE IMDB_MOVIECOUNTRIES
CREATE SEQUENCE countryid
  INCREMENT 1
  START 1
  MINVALUE 1
  MAXVALUE 100000;

--CREAMOS LA NUEVA RELACION COUNTRIES
CREATE TABLE countries(
  countryid character varying(128) NOT NULL default nextval('countryid'::regclass),
  country character varying(128)
);

--INSERTAMOS EN COUNTRIES
INSERT INTO countries(country)(
  select distinct country from imdb_moviecountries
);

--ACTUALIZAMOS LA TABLA IMDB_MOVIECOUNTRIES
UPDATE imdb_moviecountries set country=(
  SELECT countryid from countries
  where imdb_moviecountries.country=countries.country
);

--ALTERAMOS EL NOMBRE DE LA COLUMNA PARA QUE SE ADECUE MEJOR A LA NUEVA RELACION
ALTER TABLE imdb_moviecountries RENAME COLUMN country TO countryid;

--SECUENCIA PARA ID DE IMDB_MOVIEGENRES
CREATE SEQUENCE genresid
  INCREMENT 1
  START 1
  MINVALUE 1
  MAXVALUE 100000;

--CREAMOS LA NUEVA RELACION GENRES
CREATE TABLE genres(
  genresid character varying(128) NOT NULL default nextval('genresid'::regclass),
  genre character varying(128)
);

--INSERTAMOS EN LA TABLA GENRES
INSERT INTO genres(genre)(
  select distinct genre from imdb_moviegenres
);

--ACTUALIZAMOS LA TABLA IMDB_GENRES
UPDATE imdb_moviegenres set genre=(
  SELECT genresid from genres
  where imdb_moviegenres.genre=genres.genre
);

--ALTERAMOS EL NOMBRE DE LA COLUMNA PARA QUE SE ADECUE MEJOR A LA NUEVA RELACION
ALTER TABLE imdb_moviegenres RENAME COLUMN genre TO genreid;

--SECUENCIA PARA ID DE IMDB_MOVIELANGUAGES
CREATE SEQUENCE languageid
  INCREMENT 1
  START 1
  MINVALUE 1
  MAXVALUE 100000;

--CREAMOS LA NUEVA RELACION LANGUAGES
CREATE TABLE languages(
  languageid character varying(128) NOT NULL default nextval('languageid'::regclass),
  language character varying(128)
);

--INSERTAMOS EN LA TABLA LANGUAGES
INSERT INTO languages(language)(
  select distinct language from imdb_movielanguages
);

--ACTUALIZAMOS LA TABLA IMDB_LANGUAGES
UPDATE imdb_movielanguages set language=(
  SELECT languageid from languages
  where imdb_movielanguages.language=languages.language
);

--ALTERAMOS EL NOMBRE DE LA COLUMNA PARA QUE SE ADECUE MEJOR A LA NUEVA RELACION
ALTER TABLE imdb_movielanguages RENAME COLUMN language TO languageid;


--IMDB_MOVIES
ALTER TABLE imdb_movies
ALTER COLUMN year SET NOT NULL;


--ORDERDETAIL
UPDATE orderdetail SET price = 0;

ALTER TABLE orderdetail
ADD FOREIGN KEY (orderid) REFERENCES orders(orderid);

ALTER TABLE orderdetail
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id);


--ORDERS
ALTER TABLE orders
ALTER COLUMN customerid SET NOT NULL;

ALTER TABLE orders
ALTER COLUMN tax SET NOT NULL;

ALTER TABLE orders
ADD FOREIGN KEY (customerid) REFERENCES customers(customerid);


--CUSTOMERS
ALTER TABLE customers
ALTER COLUMN email SET NOT NULL;

ALTER TABLE customers
ALTER COLUMN zip SET NOT NULL;

ALTER TABLE customers
ALTER COLUMN phone SET NOT NULL;


--IMDB_ACTORMOVIES
ALTER TABLE imdb_actormovies
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

ALTER TABLE imdb_actormovies
ADD FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid);


--INVENTORY Y PRODUCTS
ALTER TABLE inventory
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id);
ALTER TABLE products
	ADD COLUMN stock integer default 0,
	ADD COLUMN sales integer default 0;

UPDATE products SET (stock,sales) = (inventory.stock,inventory.sales)
	from inventory
	where inventory.prod_id = products.prod_id;

DROP TABLE inventory;

--ACTUALIZAR USERNAMES Y PONERLOS UNICOS
UPDATE customers set username = concat(username,'_',email)
  WHERE username in (
      SELECT username FROM customers GROUP BY username having count(*) > 1);

ALTER TABLE ONLY Customers ADD CONSTRAINT customers_username_uniq  UNIQUE (username);
