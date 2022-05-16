UPDATE orderdetail SET price = initial_price
FROM(
    SELECT products.prod_id, orders.orderid, CAST(to_char(products.price * power(0.98, (date_part('year',CURRENT_DATE) - date_part('year', orders.orderdate))), 'FM9999.9999')as FLOAT) as initial_price
    FROM products, orders, orderdetail
    WHERE products.prod_id = orderdetail.prod_id and orderdetail.orderid = orders.orderid
    ) as subconsulta
WHERE orderdetail.prod_id = subconsulta.prod_id and subconsulta.orderid = orderdetail.orderid;




--precio inicial = precio_final * (0.98^ años_diferencia)
--to_char porque son distintos tipos y los unimos en uno mismo, usando FM9999.9999
--con los '9' permitimos esa misma cantidad de números y con FM eliminamos los ceros
--o blancos que se puedan generar
--CAST para convertirlo a FLOAT, ya que es un precio
