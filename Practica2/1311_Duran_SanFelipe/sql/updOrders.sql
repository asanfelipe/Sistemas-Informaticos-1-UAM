CREATE OR REPLACE FUNCTION update_orders()
RETURNS TRIGGER AS $$

BEGIN

  IF (TG_OP = 'DELETE') THEN
    UPDATE orders SET netamount = netamount - (old.price * old.quantity) where orderid = old.orderid;
	UPDATE orders SET totalamount = CAST(to_char(netamount* (1 + tax/100), 'FM9999.9999') as FLOAT) where orderid = old.orderid;
    RETURN OLD;
  END IF;


  IF (TG_OP = 'INSERT') THEN
    UPDATE orders SET netamount = netamount + (new.price * new.quantity) where orderid = new.orderid;
	UPDATE orders SET totalamount = CAST(to_char(netamount* (1 + tax/100), 'FM9999.9999') as FLOAT) where orderid = new.orderid;
    RETURN NEW;
  END IF;


  IF (TG_OP = 'UPDATE') THEN
    UPDATE orders SET netamount = netamount - (old.price * old.quantity) where orderid = new.orderid;
    UPDATE orders SET netamount = netamount + (new.price * new.quantity) where orderid = new.orderid;
    UPDATE orders SET totalamount = CAST(to_char(netamount* (1 + tax/100), 'FM9999.9999') as FLOAT) where orderid = new.orderid;
	RETURN NEW;
  END IF;


  RETURN NULL;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS updorders ON orderdetail;
CREATE TRIGGER updorders BEFORE INSERT OR DELETE OR UPDATE ON orderdetail
  FOR EACH ROW EXECUTE PROCEDURE update_orders();


-- Al final declaramos el trigger tal y como se nos ha enseñado en teoría,y
-- la función que tiene que realizar es la siguiente:
--   Se pueden dar tres casos, cada uno tratado con un IF según sea el TG_OP.
--   Si la opción es borrar, tendremos que cambiar el netamount quitandole el precio * cantidad, de los articulos viejos.
--   Y al cambiar netamount también es necesario cambiar totalamount.
--   Si la opción es insertar, será similar a borrar, pero usando los artículos nuevos.
--   Si la opción es actualizar, primero habrá que cambiar el netamount según los artículos viejos, luego usando los nuevos,
--   y finalmente, como siempre, cambiar totalamount para que se adecúe.
