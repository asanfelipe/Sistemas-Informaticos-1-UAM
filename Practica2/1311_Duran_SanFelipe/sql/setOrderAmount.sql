CREATE OR REPLACE FUNCTION	setOrderAmount() 
    RETURNS void AS $$
	
DECLARE


BEGIN
	UPDATE orders SET netamount = sum_precio
	FROM (
		SELECT orders.orderid, sum(price * quantity) as sum_precio
		FROM orders, orderdetail
		WHERE orderdetail.orderid = orders.orderid
		GROUP BY orders.orderid
		) as subconsulta
	WHERE subconsulta.orderid = orders.orderid;
	
	UPDATE orders SET totalamount = CAST(to_char(netamount * (1 + tax/100), 'FM9999.9999') as FLOAT);
	return;


END;
$$ LANGUAGE plpgsql;

SELECT * FROM setOrderAmount();


--Para actualizar netamount solamente tenemos que sumar todos los productos que hayan en
--un pedido, teniendo en cuenta que un producto puede ser comprado varias veces (quantity).
--Y para actualziar totalamount usamos el netamount consegido y lo multiplicamos por el tax
--que se ha dado como un porcentaje, de ahi dividirlo por 100.
--Retornamos la funcion y la llamamos con el SELECT final.