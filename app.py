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
        emails = s.loads(token, salt='confirmacion-email', max_age=40)
    except SignatureExpired:
        return '<h1>El token a expirado!</h1>'
    flash('Correo confirmado, ahora puedes iniciar sesion', 'success')
    empresasModels.cambiar_estado()
    return redirect(url_for('login'))

    
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
    emailbienvenida= empresasModels.emailbienvenida(email)
    password_e = empresasModels.obtenerContraseña(password_e)
    if email1 is None:
        flash('Correo no registrado', 'error')
        return redirect(request.url)
    if email2 is None:
        flash('Correo no verificado, revisa tu correo', 'error')
        is_valid=False
    if password_e is None:
        flash('contraseña incorrecta, intente de nuevo', 'error')
        is_valid=False
    if is_valid==False:
        return render_template("login.html",
        email=email,)
    if emailbienvenida is not None:
        autenticacionCorreo.emailBienvenida(email)
        empresasModels.c_emailBienvenida(email)
    return redirect(url_for('contents_empresa'))

@app.route('/empresas/contents_empresa', methods=['GET'])
def contents_empresa():
    return render_template('empresas/empresa.html')


app.run(debug=True)