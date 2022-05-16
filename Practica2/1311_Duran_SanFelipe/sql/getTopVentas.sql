DROP FUNCTION IF EXISTS getTopVentas(integer,integer);
CREATE OR REPLACE FUNCTION getTopVentas (anio1 int, anio2 int)
  RETURNS table(anio INT, pelicula VARCHAR, ventas BIGINT) AS $$

DECLARE

BEGIN
  RETURN query
    SELECT año, subconsulta.pelicula, subconsulta.ventas
    FROM(
	 SELECT cast(date_part('year', orderdate)AS INT) AS año, imdb_movies.movietitle AS pelicula, sum(quantity) AS ventas,
                ROW_NUMBER () OVER (PARTITION BY date_part('year', orderdate)
                                    ORDER BY sum(quantity) desc, imdb_movies.movietitle asc)

         FROM imdb_movies INNER JOIN products ON imdb_movies.movieid = products.movieid
                          INNER JOIN orderdetail ON orderdetail.prod_id = products.prod_id
                          INNER JOIN orders ON orders.orderid = orderdetail.orderid

    	 WHERE date_part('year', orderdate) BETWEEN anio1 and anio2
         GROUP BY movietitle, date_part('year', orderdate)
         ORDER BY date_part('year', orderdate) asc, ventas desc
    ) as subconsulta

    WHERE row_number = 1
    ORDER BY ventas desc, pelicula;

END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTopVentas(2014, 2020)


-- Para conseguir esta query necesitaremos de varias tablas de la DB, en concreto imdb_movies,
-- products, orderdetail y orders, que se van enlazando por claves primarias y foráneas existentes.
-- En cuanto a la restricción del 'where' será necesario que el año, que sacamos con date_part, se
-- encuentre entre los dos años que se le pasan por parámetro. Lo agruparemos por el título de la
-- película y por la fecha que fueron compradas; y para odenarlas lo aremos por la fecha de manera
-- ascendente y las ventas de manera descendente. Por último, para completar esta subconsulta,
-- seleccionaremos el año que fueron compradas, el título de las películas, una suma de la cantidad
-- de veces que se ha comprado cada película y, por último, haremos uso del row_number para poder partir
-- la query en varios grupos, haciendolo por los años y ordenando por las ventas y el título de la película.
-- Al ordenar el row_number por las ventas de manera descendente conseguiremos que de cada año, la película
-- con más ventas tenga asignado el row_number = 1. Gracias a esto, luego en la consulta general podemos restringir
-- a aquellos que solamente tengan este row_number, que se corresponderan con las películas más vendidas por cada año.
-- Además, ordenamos por el número de ventas y el título de la película en caso de haber empate y mostramos todo lo
-- que se nos pide.
-- A la función la llamamos con los años de los que hay registro en la base de datos y así se puede observar el película
-- más vendida de 2014 a 2020.
