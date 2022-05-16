DROP FUNCTION IF EXISTS getTopMonths(integer, integer);
CREATE OR REPLACE FUNCTION getTopMonths (num_prod int, max_amount int)
  RETURNS table(anio DOUBLE PRECISION, mes DOUBLE PRECISION, importe NUMERIC, productos BIGINT) AS $$

DECLARE

BEGIN
  RETURN query
    SELECT date_part('year', orders.orderdate) as año, date_part('month', orders.orderdate) as mes, sum(totalamount) as importe, sum(quantity) as productos
    FROM orders INNER JOIN orderdetail on orders.orderid = orderdetail.orderid
    GROUP BY date_part('year', orders.orderdate), date_part('month', orders.orderdate)
    HAVING sum(totalamount) > max_amount or sum(quantity) > num_prod
    ORDER BY date_part('year', orders.orderdate), date_part('month', orders.orderdate);

END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTopMonths(19000, 320000)

-- Necesitaremos las tablas de orders y orderdetail para sacar el totalamount y quantity, y las
-- relacionaremos por el orderid. Las agruparemos y las ordenaremos por el año y mes, sacando esos datos
-- con el date_part y tendra que cumplir una u otra clausula del having.
-- De esto seleccionaremos el año, mes, suma de totalamount y suma de quantity.

--Probamos la funcion con los datos que nos indica el guión
