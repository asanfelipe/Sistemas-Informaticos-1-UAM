--Apartado b) creacion de la nueva columna promo
alter table customers add promo integer;
--Apartado c) creacion del trigger
CREATE OR REPLACE FUNCTION promo() returns TRIGGER
language plpgsql
as $$
DECLARE
BEGIN
update orders set totalamount = totalamount- totalamount * promo/100
	from customers
	inner join orders on customer.customerid=orders.customerid
	where customerid= NEW.customerid and status = null;
	return new;
	--Apartado d) modificar el trigger para que haga un sleep con pg_sleep
	perform pg_sleep(15);
END;
$$;

create trigger updPromo after update or insert on customers
for each row execute procedure promo();


