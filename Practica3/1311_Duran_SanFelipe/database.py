import os
import sys, traceback

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select


db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})
db_meta = MetaData(bind=db_engine,reflect = True)
db_connect = db_engine.connect()

def db_topUSA():
    try:
        db_result = db_connect.execute("select distinct movietitle as title, year,\
        array_to_string(array_agg(distinct genre), ', ') as genres,\
        array_to_string(array_agg(distinct actorname), '; ') as actors\
        from imdb_movies\
        natural join imdb_moviecountries\
        natural join imdb_moviegenres\
        natural join imdb_actormovies\
        natural join imdb_actors\
        where country='USA' group by movietitle, year order by year desc, movietitle desc limit 800;")
        return list(db_result)
    except:
        print("Se va por except")
        return []

def db_getDirectors(movietitle):
    try:
        db_result = db_connect.execute("select directorname from imdb_directormovies natural join imdb_directors natural join imdb_movies where movietitle='"+movietitle+"';")
        return list(db_result)
    except:
        return []

def db_register(firstname, lastname, address1, address2, city, state, zip, country, region, email, phone, creditcardtype, creditcard, creditcardexpiration, username, password, age, income, gender):
    try:

        # Conseguimos el último id de la tabla customers y le pasaremos a la consulta el siguiente valor para que no haya duplicidad en los id
        id = db_connect.execute("select customerid from customers order by customerid desc limit 1;")


        db_result = db_connect.execute("insert into customers values ("+str(list(id)[0][0] + 1)+", '"+firstname+"', '"+lastname+"', '"+address1+"', '"+address2+"', '"+city+"', '"+state+"', '"+zip+"', '"+country+"', '"+region+"', '"+email+"', '"+phone+"', '"+creditcardtype+"', '"+creditcard+"', '"+creditcardexpiration+"', '"+username+"', '"+password+"', '"+age+"', '"+str(income)+"', '"+gender+"');")

        return db_result
    except:
        if db_connect is not None:
            db_connect.close()
        print("Error at register.")
        return -1

def db_login(username):
    try:

        db_result = db_connect.execute("select password from customers where username = '"+username+"';")

        return list(db_result)
    except:
        if db_connect is not None:
            db_connect.close()
        return -1

def db_findMovie(busqueda):
    try:
        # Permitimos que la busqueda muestre que lo que se ha introducido tenga la primera letra mayúscula o no
        busqueda_mayus = busqueda[0].upper() + busqueda[1:]
        busqueda_minus = busqueda.lower()

        db_result = db_connect.execute("select prod_id,movietitle,year,price from products inner join imdb_movies on imdb_movies.movieid = products.movieid where movietitle like '%%"+str(busqueda_mayus)+"%%' or movietitle like '%%"+str(busqueda_minus)+"%%';")

        return list(db_result)
    except:
        if db_connect is not None:
            db_connect.close()
        return []

def db_getMovie(id):
    try:
        db_result = db_connect.execute("select prod_id,movietitle,year,price from products inner join imdb_movies on imdb_movies.movieid = products.movieid where prod_id ="+str(id)+";")

        return list(db_result)[0]
    except:

        return []

def db_getCatalogue():
    try:
        db_result = db_connect.execute("select prod_id,movietitle,price from products inner join imdb_movies on imdb_movies.movieid = products.movieid order by prod_id limit 20;")

        return db_result
    except:

        return []

def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
	dbr=[]
	
	db_conn = db_engine.connect()
	
	try:
		if bSQL:
			dbr.append("Se ejecuta a traves de SQL")
			result = db_conn.execute("BEGIN;")
			dbr.append("BEGIN")
			result = db_conn.execute("delete from orderdetail where exists orderid in (select orderid from orders where customerid = "+customerid+")")
			dbr.append("Se borrarán los datos de los pedidos del cliente: "+customerid)
			
			if bCommit:
				result = db_conn.execute("COMMIT;")
				dbr.append("Commit intermedio. Se inicia otra transaccion")
				result = db_conn.execute("BEGIN;")
			if not bFallo:
				result = db_conn.execute("delete from orders where customerid ="+customerid)
				dbr.append("Se borrarán los pedidos del cliente: "+customerid)
			result = db_conn.execute("delete from customers where customerid ="+customerid)
			dbr.append("Se borrará el cliente")
			result = db_conn.execute("COMMIT;")
			dbr.append("Transaccion finalizada correctamente.")
		else:
			dbr.append("Se ejecuta a traves de SQL ALCHEMY")
			alchemy = db_conn.begin()
			dbr.append("BEGIN")
			result = db_conn.execute("delete from orderdetail where orderid in (select orderid from orders where customerid = "+customerid+")")
			dbr.append("Datos de los pedidos del cliente "+customerid+" borrados.")
			
			if bCommit:
				alchemy.commit()
				dbr.append("Commit intermedio. Se inicia otra transaccion")
				alchemy = db_conn.begin()
			if not bFallo:
				result = db_conn.execute("delete from orders where customerid ="+customerid)
				dbr.append("Pedidos del cliente "+customerid+" borrados.")
			result = db_conn.execute("delete from customers where customerid ="+customerid)
			dbr.append("Cliente borrado")
			alchemy.commit()
			dbr.append("Transaccion finalizada correctamente.")

	except Exception as e:
		dbr.append("Error en la transaccion. Haciendo rollback.")
		if bSQL:
			result = db_conn.execute("rollback;")
		else:
			alchemy.rollback()
			
	dbr.append("Cerramos la conexión con la base de datos.")
	db_conn.close()

	return dbr
