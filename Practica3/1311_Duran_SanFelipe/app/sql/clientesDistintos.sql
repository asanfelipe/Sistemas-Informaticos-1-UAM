--Apartado a) de creacion de consulta
select count(distinct customerid) as Suma
   from orders 
   where date_part('month',orderdate)= 04 and
   date_part('year',orderdate) = 2015 and totalamount > 100;
--Apartado c) de creacion de indices
create index orderdate_index on orders (orderdate); --Este indice no tiene impacto en el coste de la consulta
create index totalamount_index on orders (totalamount); --Este indice tiene un impacto positivo en el coste de la consulta
--Apartado f) modificacion de consulta
explain
select count(distinct customerid) as Suma
   from orders 
   where date_part('month',orderdate)= 04 and
   date_part('year',orderdate) = 2015 and totalamount > 100;
