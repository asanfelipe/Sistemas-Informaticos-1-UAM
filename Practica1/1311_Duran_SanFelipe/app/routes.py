#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
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
    catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies_filtro = ""

    if session.get('username') is not None:
        username = session['username']
    else:
        username = ""

    return render_template('index.html', title="Index", error="", username=username, movies=catalogue['peliculas'], filtrar="", categoria="", movies_filtro="")


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = ""
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    # aqui se deberia validar con fichero .dat del usuario
    if request.method == 'POST':
        username = request.form['name']
        psw = request.form['psw']
        if username == "":
            error = "Debe escribir un nombre de usuario"
            return render_template('login.html', username="", error=error, username_cookie=request.cookies.get('userID'))
        if not os.path.exists(this_dir+"/usuarios/"+username):
            error = "El usuario especificado no existe"
            return render_template('login.html', username="", error=error, username_cookie=request.cookies.get('userID'))

        username = json.load(open(this_dir+"/usuarios/"+username+"/datos.dat"))
        if username["contrasena"] == hashlib.sha512(psw.encode('utf-8')).hexdigest():
            session['username'] = username
            session.modified = True
            resp = make_response(redirect(url_for('usuario')))
            return resp

        error = "La contraseña no es correcta"

    if session.get('username') is not None:
        username = session['username']
    else:
        username = ""
    return render_template('login.html', username=username, error=error, username_cookie=request.cookies.get('userID'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/registro', methods=['GET', 'POST'])
def validacion():
    error = ""
    if request.method == 'POST':
        username = request.form['name']
        psw = request.form['psw']
        email = request.form['email']
        Tarjeta = request.form['card']

        if os.path.exists(this_dir+"/usuarios/"+username):
            error = "El usuario ya existe. Escoja otro nombre de usuario"
        else:
            os.mkdir(this_dir+"/usuarios/"+username)
            dict_usuario = {}
            dict_usuario["username"] = username
            dict_usuario["contrasena"] = hashlib.sha512(psw.encode('utf-8')).hexdigest()
            dict_usuario["E-mail"] = email
            dict_usuario["Tarjeta"] = Tarjeta
            dict_usuario["Saldo"] = random.randint(0, 101)
            file = open(this_dir+"/usuarios/"+username+"/datos.dat", "w")
            json.dump(dict_usuario, file)
            file.close()

            file = open(this_dir+"/usuarios/"+username+"/historial.json", "w")
            json.dump([], file)
            file.close()
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
    catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    for item in catalogue['peliculas']:
        if item['id'] == id:
            detalle = item

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
    catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    dict_busq = {}

    if request.method == 'POST':
        filtrar = request.form['filtrar']
        categoria = request.form['categoria']
        for item in catalogue['peliculas']:
            if filtrar.lower() in item['titulo'].lower() and item['categoria'] == categoria:
                titulo = item['titulo']
                dict_busq[titulo] = item

        if session.get('username') is not None:
            username = session['username']

        else:
            username = ""

        return render_template('index.html', username=username, error="", movies_filtro=dict_busq, filtrar=filtrar, categoria=categoria)

    # Si se usa la barra lateral, se buscará con el método GET
    else:
        filtrar = request.args.get('filtrar')
        if filtrar is None:
            filtrar = ""
        categoria = request.args.get('categoria')
        for item in catalogue['peliculas']:
            if filtrar.lower() in item['titulo'].lower() and item['categoria'] == categoria:
                titulo = item['titulo']
                dict_busq[titulo] = item

        if session.get('username') is not None:
            username = session['username']

        else:
            username = ""

        return render_template('index.html', username=username, error="", movies_filtro=dict_busq, filtrar=filtrar, categoria=categoria)
