CREATE OR REPLACE FUNCTION update_inventory()
RETURNS TRIGGER AS $$

DECLARE
  stock_ INT;
  i RECORD;  -- Record es un tipo de dato para gestionar filas de tablas

BEGIN

  IF (TG_OP = 'UPDATE') THEN

	  FOR i IN SELECT prod_id, quantity
	           FROM orderdetail
			   WHERE orderid = new.orderid
	  LOOP
	    UPDATE products SET stock = stock - i.quantity WHERE prod_id = i.prod_id;
	    UPDATE products SET sales = sales + i.quantity WHERE prod_id = i.prod_id;

        SELECT stock INTO stock_ FROM products WHERE prod_id = i.prod_id;
	    IF (stock_ == 0) THEN
	      INSERT INTO alertas VALUES (i.prod_id);
	    END IF;
	  END LOOP;
   END IF;
 RETURN NEW;

END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS updinventory ON orders;
CREATE TRIGGER updinventory BEFORE UPDATE ON orders
  FOR EACH ROW EXECUTE PROCEDURE update_inventory();


-- Al final declaramos el trigger tal y como se nos ha enseñado en teoría,y
-- la función que tiene que realizar es la siguiente:
--   Si el TG_OP es un update y si el status del order ha cambiado de NULL a otro
--   entonces por cada prod_id y la cantidad en orderdetail (restringiendo por el prod_id),
--   actualizamos el stock, restándole la cantidad de veces que se haya comprado el producto
--   y actualizamos el sales, sumándole nuevamente la misma cantidad.
--   A parte, copiamos el valor de stock en una variable que denominamos 'stock_' para observar si
--   al modificar el estos con las líneas superiores se ha llegado a 0. Si ocurre entonces
--   metemos en la tabla de alertas el valor del prod_id que ha alcanzado ese stock.
