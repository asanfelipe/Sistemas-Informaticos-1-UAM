#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
import database
from flask import render_template, request
from flask import url_for, redirect, session, make_response
import json
import random
import os
import hashlib

this_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
@app.route('/index')
def index():

    movies_filtro = ""
    movies = database.db_getCatalogue()

    topventas = database.db_getTopVentas()

    if session.get('username') is not None:
        username = session['username']
    else:
        username = ""

    return render_template('index.html', title="Index", error="", username=username, movies=movies, filtrar="", movies_filtro="", topventas=topventas)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = ""

    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']

        if username == "":
            error = "Debe escribir un nombre de usuario"
            return render_template('login.html', username="", error=error, username_cookie=request.cookies.get('userID'))

        login = database.db_login(username)
        if login == -1 or str(login) == "[]":
            error = "Datos de autenticación incorrectos."


        if login[0][0] == password:
            session['username'] = username
            session.modified = True
            resp = make_response(redirect(url_for('usuario')))
            return resp

        else:
            error = "Datos de autenticación incorrectos."
            return render_template('login.html', username="", error=error, username_cookie=request.cookies.get('userID'))

    if session.get('username') is not None:
        username = session['username']
    else:
        username = ""

    return render_template('login.html', username=username, error=error, username_cookie=request.cookies.get('userID'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/registro', methods=['GET', 'POST'])
def validacion():
    error = ""
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        country = request.form['country']
        region = request.form['region']
        phone = request.form['phone']
        creditcard = request.form['creditcard']
        creditcardtype = request.form['creditcardtype']
        creditcardexpiration = request.form['creditcardexpiration']
        age = request.form['age']
        gender = request.form['gender']
        income = random.randint(0, 101)

        register = database.db_register(firstname, lastname, address1, address2, city, state, zip, country, region, email, phone, creditcardtype, creditcard, creditcardexpiration, username, password, age, income, gender)

        if register == -1:
            error = "El usuario ya existe."
        else:
            error = "¡Usuario creado con éxito! Ya puedes entrar a tu cuenta."

    if session.get('username') is not None:
        username = session['username']
    else:
        username = ""

    return render_template('registro.html', error=error, username=username)


@app.route('/usuario', methods=['POST', 'GET'])
def usuario():
    if session.get('username') is not None:
        username = session['username']
    else:
        username = ""

    return render_template('usuario.html', username=username, error="", title="Historial de Usuario")


@app.route('/carrito')
def carrito():
    if session.get('username') is not None:
        username = session['username']

    else:
        username = ""

    return render_template('carrito.html', username=username, error="", title="Carrito")


@app.route('/detalles/<int:id>')
def detalles(id):

    detalle = database.db_getMovie(id)

    if session.get('username') is not None:
        username = session['username']

    else:
        username = ""

    return render_template('detalles.html', title="Detalles", error="", username=username, movies=detalle)


@app.route('/ajax')
def ajax():
    return str(random.randint(1, 100))


@app.route('/busqueda', methods=['POST', 'GET'])
def busqueda():

    topventas = database.db_getTopVentas()

    if request.method == 'POST':

        filtrar = request.form['filtrar']
        busqueda = database.db_findMovie(filtrar)

        if session.get('username') is not None:
            username = session['username']

        else:
            username = ""

        return render_template('index.html', username=username, error="", movies_filtro=busqueda, filtrar=filtrar, topventas=topventas)
