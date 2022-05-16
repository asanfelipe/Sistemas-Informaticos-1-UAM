EXPLAIN
select count(*)
from orders
where status is null;

EXPLAIN
select count(*)
from orders
where status ='Shipped';

CREATE INDEX status_orders on orders(status);

EXPLAIN
select count(*)
from orders
where status is null;

EXPLAIN
select count(*)
from orders
where status ='Shipped';

ANALYZE;

EXPLAIN
select count(*)
from orders
where status is null;

EXPLAIN
select count(*)
from orders
where status ='Shipped';

EXPLAIN 
select count(*)
from orders
where status ='Paid';

EXPLAIN
select count(*)
from orders
where status ='Processed';