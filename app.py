from asyncio.windows_events import NULL
from click import edit
from flask import Flask, render_template, request, redirect, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import hashlib
from models import empresasModels
from controllers import autenticacionCorreo, empresaControllers, validarDatos, msgWpp
from controllers.forms import LoginForm, EditUser
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
    imagen = request.files['imagen']
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
    img = empresaControllers.nombreImagen(imagen)
    imagen.save('./static/resources/imagen_empresa/'+str(img))


    token = s.dumps(email, salt='confirmacion-email')
    link = url_for('confirmar_email', token=token, _external=True)
    autenticacionCorreo.enviarEmail(email,link)
    password = hashlib.sha1(password.encode()).hexdigest()
    empresasModels.crearEmpresa(imagen='/static/resources/imagen_empresa/'+img, nombre_empresa=nombre_empresa, contacto=contacto, direccion=direccion, email=email, password=password, descripcion=descripcion)
    flash('Revisa tu buzon para continuar', 'success')
    return redirect(url_for('login'))

 

@app.route('/login', methods=['GET', 'POST']) 

def login():
    form = LoginForm()
    if form.validate_on_submit():
        is_valid=True
        email =form.email.data
        password = form.password.data
        password_e = hashlib.sha1(password.encode()).hexdigest()
        #empresasModels.delete_regiters(email)
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
            form=form)

        session['user_id'] = email2
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout') 
def logout():
    session.clear()

    return redirect(url_for('login'))

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

@app.route('/empresas/empresaPagina')
def home():

    id=empresaControllers.obtenerId(session)
    datos=empresasModels.obtenerEmpresa(id)
    productos = empresasModels.obtenerProductos(id)
    return render_template('empresas/home.html', datos = datos, productos=productos[0][0])

@app.route('/empresas/empresaPagina/configuracion', methods=['GET', 'POST'])
def editarEmpresa():
    if request.method == 'GET':
            id=empresaControllers.obtenerId(session)
            datos=empresasModels.obtenerEmpresa(id)
            form = EditUser(
            name=datos[2],
            phone = datos[3],
            address=datos[4],
            description=datos[7]
             ) 
            return render_template('empresas/editarEmpresa.html', datos=datos, form=form)
    #is_valid=True
    imagen = request.files['img']
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    description = request.form.get('description')
    password = request.form.get('password')
    if imagen:
            img = empresaControllers.nombreImagen(imagen)
            imagenn='/static/resources/imagen_empresa/'+img
            imagen.save('./static/resources/imagen_empresa/'+img)
    else:
        imagenn = None
    
    if password:
        if not (validarDatos.contraseñaValidacion(password)):
            return redirect(request.url)
        else:
            password = hashlib.sha1(password.encode()).hexdigest()
        
    else:
        password = None

    try:
        empresasModels.editarEmpresa(imagenn,name, phone, address, password, description)
        flash('Se ha editado su usuario correctamente', 'success')
    except:
        flash('Error al editar el usuario ', 'error')
        return redirect(url_for('editarEmpresa'))
    return redirect(url_for('editarEmpresa'))


@app.route('/empresas/empresaPagina/categorias')
def categorias():
    id=empresaControllers.obtenerId(session)
    datos=empresasModels.obtenerEmpresa(id)
    categorias = empresasModels.listarCategoria(id)
    return render_template('/categorias/listarCategoria.html', categorias=categorias, datos = datos)

@app.route('/empresas/empresaPagina/categorias/eliminar/<string:id>')
def eliminarCategoria(id):
    if empresasModels.verificarCategoriaProducto(id):
        flash("No puedes eliminar esta categoria", 'error')
    else:
        empresasModels.eliminarCategoria(id)
    return redirect(url_for('categorias'))

          
   
@app.route('/empresas/empresaPagina/categorias/crear', methods=['GET', 'POST'])
def crearCategoria():
    id=empresaControllers.obtenerId(session)
    if request.method == 'GET':
        datos=empresasModels.obtenerEmpresa(id)
        return render_template('/categorias/crearCategoria.html', datos = datos)
    nombreCategoria = request.form.get('nombreCategoria').upper()
    if(nombreCategoria==""):
        flash('El campo nombre categoria es requerido', 'error')
        return redirect(request.url)
    if empresasModels.obtenerCategoria(nombreCategoria, id):
        flash('Ya existe esta categoria', 'error')
        return redirect(request.url)
    try:
        empresasModels.crearCategoria(id,nombreCategoria)
    except:
        flash('No se ha podido guardar la categoria', 'error')
        return redirect(request.url)
    flash('Se creo correctamente la categoria', 'success')
    return redirect(url_for('categorias'))

@app.route('/empresas/empresaPagina/menu')
def menu():
    id=empresaControllers.obtenerId(session)
    datos=empresasModels.obtenerEmpresa(id)
    productos=empresasModels.listarProductos(id)
    return render_template('productos/listarProductos.html', productos=productos, datos= datos)


@app.route('/empresas/empresaPagina/menu/agregarProducto', methods=['GET', 'POST'])
def crearProducto():
    if request.method == 'GET':
        id=empresaControllers.obtenerId(session)
        datos=empresasModels.obtenerEmpresa(id)
        estado= empresasModels.obtenerEstado()
        categorias=empresasModels.listarCategoria(id)
        return render_template('productos/crearProducto.html', categorias=categorias, estado=estado, datos=datos)
    idEmpresa= str(session['user_id'][0])
    nombre= request.form.get('name').upper()
    precio = request.form.get('price')
    categoria= request.form.get('category')
    disponibilidad= request.form.get('avaliability')
    imagen = request.files['image']
    descripcion= request.form.get('description')
    try: 
        img = empresaControllers.nombreImagen(imagen)
        empresasModels.crearProducto(idEmpresa=idEmpresa, categoria=categoria, disponibilidad=disponibilidad, nombre=nombre, precio=precio,imagen='/static/resources/imagen_empresa/'+img, descripcion= descripcion)
    except:
        flash('No se ha podido guardar el producto', 'error')
    imagen.save('./static/resources/imagen_empresa/'+str(img))
    flash('Se ha creado el producto correctamente', 'success')
    return redirect(url_for('menu'))
    
@app.route('/empresas/empresaPagina/menu/editarProducto/<string:id>', methods=['GET','POST'])
def editarProducto(id):
    if request.method == 'GET':
        ids=empresaControllers.obtenerId(session)
        datos=empresasModels.obtenerEmpresa(id)
        categorias=empresasModels.listarCategoria(ids)
        estado= empresasModels.obtenerEstado()
        productos=empresasModels.editarProducto(id)
        return render_template('/productos/editarProducto.html', producto = productos, estado = estado, categorias=categorias, datos = datos)

    nombre= request.form.get('name').upper()
    precio = request.form.get('price')
    categoria= request.form.get('category')
    disponibilidad= request.form.get('avaliability')
    imagen = request.files['image']
    descripcion = request.form.get('description')
    
    if not categoria.isdigit():
        categoria = None
    if not disponibilidad.isdigit():
        disponibilidad = None
    if imagen:
            img = empresaControllers.nombreImagen(imagen)
            imagenn='/static/resources/imagen_empresa/'+img
            imagen.save('./static/resources/imagen_empresa/'+img)
    else:
        imagenn = None  

    try:
        empresasModels.editarProductosCargar(categoria ,disponibilidad, nombre, precio, imagenn, id, descripcion)
        flash('Se ha editado el producto correctamente', 'success')
    except:
        flash('No se ha podido editado el producto ', 'error')
        return redirect(url_for('menu'))
    return redirect(url_for('menu'))

 
@app.route('/empresas/empresaPagina/menu/eliminar_producto/<string:id>')
def eliminarProducto(id):
    empresasModels.eliminarProducto(id)
    
    return redirect(url_for('menu'))

@app.route('/empresas')
def empresas():
    productos=empresasModels.listarTodosProductos()
    return render_template('carta/empresas.html', productos=productos)
@app.route('/productos_empresas')
def carta():
    productos=empresasModels.listarTodosProductos()
    return render_template('carta/index.html', productos=productos)

@app.route('/pedido/finalizar', methods=['GET','POST'])
def pedido():
    if request.method == 'GET':
        return render_template('usuarios/finalizarPago.html')

    numeroTargeta = request.form.get('inputNumero')
    nombre = request.form.get('inputNombre')
    cvv = request.form.get('inputCCV')
    año = request.form.get('year')
    mes = request.form.get('mes')

    if numeroTargeta and nombre and cvv and año and mes:
        flash("Pago hecho con exito" , 'success')
        msgWpp.enviarWpp(numero)
    else:
        return redirect(url_for('pedido'))

    return redirect(url_for('carta'))



app.run(debug=True)