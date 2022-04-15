from os import link
from urllib.request import Request
from django.contrib import messages
from flask import Flask, render_template, request, redirect, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import hashlib
from models import empresasModels, validarDatos, autenticacionCorreo

app = Flask(__name__)
app.secret_key = 'spbYO0JJOPUFLUikKYbKrpS5w3KUEnab5KcYDdYb'
s = URLSafeTimedSerializer('Thisisasecret!')
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/confirmar_email/<token>', methods=['GET'])
def confirmar_email(token):
    try:
        email = s.loads(token, salt='confirmacion-email', max_age=40)
    except SignatureExpired:
        return render_template('reenviarToken.html')
    empresasModels.cambiar_estado(email)
    autenticacionCorreo.emailBienvenida(email)
    flash('Correo confirmado, ahora puedes iniciar sesion', 'success')
    return redirect(url_for('login',))

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

    email_empresa = empresasModels.obtenerEmail(email)
    name_empresa = empresasModels.obtenerNombreEmpresa(nombre_empresa)
    
    is_valid = True
    

    if(nombre_empresa == "" or email == ""):
        flash('HAY CAMPOS QUE SON REQUERIDOS', 'error')
        is_valid = False

    if(len(email_empresa) > 0 or len(name_empresa) > 0):
        flash('Ya existe una empresa con estos datos', 'error')
        is_valid = False
    
    if (not validarDatos.contraseñaValidacion(password)): 
        flash('La contraseña debe cumplir con los requisitos', 'error')
        is_valid = False

    if is_valid == False:
        return render_template('empresas/register.html',
        contacto=contacto,
        direccion = direccion,
        descripcion = descripcion,
        imagen = imagen,
        )

    token = s.dumps(email, salt='confirmacion-email')
    link = url_for('confirmar_email', token=token, _external=True)
    autenticacionCorreo.enviarEmail(email,link)
    password = hashlib.sha1(password.encode()).hexdigest()
    empresasModels.crearEmpresa(imagen, nombre_empresa, contacto, direccion, email, password, descripcion)
    flash('Revisa tu buzon para continuar', 'success')
    return redirect(url_for('login'))

 

@app.route('/login', methods=['GET', 'POST']) 

def login():
    if request.method == 'GET':
        return render_template('login.html')
    is_valid=True
    email = request.form.get('email')
    password = request.form.get('password')
    password_e = hashlib.sha1(password.encode()).hexdigest()
    #empresasModels.delete_regiters(email)
    if (email == "" or password == ""):
        flash('campos requeridos', 'error')
        return redirect(request.url)
    email1 = empresasModels.obtenerEmail0(email)
    email2 = empresasModels.obtenerEmail2(email)
    password_e = empresasModels.obtenerContraseña(password_e)
    if email1 is None:
        flash('Correo no registrado', 'error')
        return redirect(request.url)
    if email2 is None:
        flash('Cuenta no verificada, revisa tu buzon', 'error')
        is_valid=False
    if email2 is not None and password_e is None:
        flash('contraseña incorrecta, intente de nuevo', 'error')
        is_valid=False
    if is_valid==False:
        return render_template("login.html",
        email=email,)
    return redirect(url_for('contents_empresa'))

@app.route('/recuperarContraseña', methods=['GET', 'POST']) 
def recuperarContraseña():
    if request.method == 'GET':
        return render_template('recuperarContraseña.html')
    email = request.form.get('email')
    email_c = empresasModels.obtenerEmail0(email)
    if email_c is None:
        flash('Este correo no existe, intente con otro', 'error')
        return redirect(request.url)
    token2 = s.dumps(email, salt='recuperar-contraseña')
    link = url_for('recuperarContraseñaLink', token2=token2, _external=True)
    autenticacionCorreo.emailRecuperacionContraseña(email,link)
    flash('Se ha enviado a tu correo las instrucciones para recuperar tu contraseña', 'success')
    return redirect(url_for('login'))

@app.route('/recuperarContraseñaLink/<token2>', methods=['GET', 'POST'])
def recuperarContraseñaLink(token2):
    try:
        email = s.loads(token2, salt='recuperar-contraseña')
    except SignatureExpired:
        return render_template("reenviarToken.html")
    link = url_for('cambiarContraseña', email=email, _external=True)
    return '<a href="{}">reestablece tu contraseña aqui</a>'.format(link)

@app.route('/cambiarContraseña/<email>', methods=['GET', 'POST'])
def cambiarContraseña(email):
    if request.method == 'GET':
        return render_template("cambiarContraseña.html")
    else:
        password = request.form.get('password')
        password_e = hashlib.sha1(password.encode()).hexdigest()
        if (password == ""):
            flash('Invalid Password', 'error')
            return redirect(request.url)
        if (not validarDatos.contraseñaValidacion(password)): 
            flash('La contraseña debe cumplir con los requisitos', 'error')
            return redirect(request.url)
        empresasModels.cambiarContraseña(email,password_e)
        flash('Se ha restablecido correctamente su contraseña', 'success')
        return redirect(url_for('login'))

@app.route('/empresas/contents_empresa', methods=['GET'])
def contents_empresa():
    if request.method == 'GET':
        return render_template('empresas/empresa.html')



app.run(debug=True)