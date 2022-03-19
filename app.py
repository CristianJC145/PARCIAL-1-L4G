from ast import Return
from flask import Flask, render_template, request, redirect, url_for, flash, session
#import sqlite3
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'spbYO0JJOPUFLUikKYbKrpS5w3KUEnab5KcYDdYb'
#db = sqlite3.connect('data.db', check_same_thread=False)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port=3306,
    database='carta_virtual'
)
db.autocommit = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def registrar_empresa():
    if request.method == 'GET':
      return render_template('empresas/register.html')

    nombre_empresa = request.form.get('nombre-empresa')
    contacto = request.form.get('contacto')
    email = request.form.get('email')
    direccion = request.form.get('direccion')
    descripcion = request.form.get('descripcion')
    imagen = request.form.get('imagen')
    password = request.form.get('password')

    password = hashlib.sha1(password.encode()).hexdigest()
     
    cursor=db.cursor()
    email_empresa = cursor.execute('select * from empresa where email = %s', (email,))
    email_empresa = cursor.fetchall()

    cursor=db.cursor()
    name_empresa = cursor.execute('select * from empresa where nombre_empresa = %s', (nombre_empresa,))
    name_empresa = cursor.fetchall()

    if(nombre_empresa == "" or email == ""):
        flash('HAY CAMPOS QUE SON REQUERIDOS', 'error')
        return redirect(request.url)
    
    if not contacto.isdigit():
        flash("El precio debe ser un numero")

    if(len(email_empresa) > 0 or len(name_empresa) > 0):
        flash('Ya existe una empresa con estos datos', 'error')
        return redirect(request.url)

    try:
        cursor = db.cursor()
        cursor.execute("""insert into empresa(
                imagen,
                nombre_empresa,
                contacto,
                direccion,
                email,
                contraseña,
                descripcion
            )values (%s,%s,%s,%s,%s,%s,%s)
        """, (imagen, nombre_empresa, contacto, direccion, email, password, descripcion,))

        db.commit()
    except:
        flash('No se ha podido guardar el usuario', 'error')
        return redirect(url_for('registrar_empresa'))

    flash('Usuario creado correctamente', 'success')

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST']) 

def login():
    if request.method == 'GET':
        return render_template('login.html')


    email = request.form.get('email')
    password = request.form.get('password')
    password = hashlib.sha1(password.encode()).hexdigest()

    cursor=db.cursor()
    email = cursor.execute("""select * from empresa where 
        email = %s""", (email,))
    email = cursor.fetchone()

    validar_contraseñas = cursor.execute("select * from empresa where contraseña = %s""", (password,))
    validar_contraseñas = cursor.fetchone()

    if email is None:
        flash('Correo no registrado', 'error')
        return redirect(request.url)

    if validar_contraseñas is None:
        flash('Contraseña incorrecta', 'error')
        return render_template("login.html",
            email = email,
        )
    

    return redirect(url_for('contents_empresa'))

@app.route('/empresas/contents_empresa', methods=['GET'])
def contents_empresa():
    return render_template('empresas/empresa.html')

app.run(debug=True)