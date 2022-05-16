import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine,reflect = True)
db_connect = db_engine.connect()


def db_register(firstname, lastname, address1, address2, city, state, zip, country, region, email, phone, creditcardtype, creditcard, creditcardexpiration, username, password, age, income, gender):
    try:

        db_connect = db_engine.connect()

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
        db_connect = db_engine.connect()
        db_result = db_connect.execute("select password from customers where username = '"+username+"';")

        return list(db_result)
    except:
        if db_connect is not None:
            db_connect.close()
        return -1

def db_findMovie(busqueda):
    try:
        db_connect = db_engine.connect()

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
        db_connect = db_engine.connect()
        db_result = db_connect.execute("select prod_id,movietitle,year,price from products inner join imdb_movies on imdb_movies.movieid = products.movieid where prod_id ="+str(id)+";")

        return list(db_result)[0]
    except:

        return []

def db_getCatalogue():
    try:
        db_connect = db_engine.connect()
        db_result = db_connect.execute("select prod_id,movietitle,price from products inner join imdb_movies on imdb_movies.movieid = products.movieid order by prod_id limit 20;")

        return db_result
    except:

        return []


def db_getTopVentas():
    try:
        db_connect = db_engine.connect()
        db_result = db_connect.execute("select * from getTopVentas("+"2014"+","+"2020"+");").fetchall()

        return db_result
    except:
        print("Error")

        return []
