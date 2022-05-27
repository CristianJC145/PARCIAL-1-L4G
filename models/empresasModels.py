from unicodedata import digit, numeric
from config.database import db
def obtenerEmail0(email):
    cursor = db.cursor()
    cursor.execute('select * from empresa where email = %s', (email,)) 
    emailEmpresa=cursor.fetchone()
    return emailEmpresa

def obtenerEmail(email):
    cursor = db.cursor()
    cursor.execute('select * from empresa where email = %s', (email,)) 
    emailEmpresa=cursor.fetchall()
    return emailEmpresa

def obtenerEmail2(email):
    cursor = db.cursor()
    cursor.execute("select * from empresa where estado = 1 and email = %s", (email,)) 
    emailEmpresa2=cursor.fetchone()
    return emailEmpresa2

def obtenerNombreEmpresa(nombre_empresa):
    cursor = db.cursor()
    cursor.execute('select * from empresa where nombre_empresa = %s', (nombre_empresa,))
    nombreEmpresa=cursor.fetchall()
    return nombreEmpresa

def obtenerContraseña(password):
    cursor = db.cursor()
    cursor.execute("select * from empresa where estado = 1 and contraseña = %s",(password,))
    validarContraseñas = cursor.fetchone()
    return validarContraseñas

def crearEmpresa(imagen, nombre_empresa, contacto, direccion, email, password, descripcion):
    cursor = db.cursor()
    cursor.execute("""insert into empresa(
                imagen,
                nombre_empresa,
                contacto,
                direccion,
                email,
                contraseña,
                descripcion,
                estado,
                emailbienvenida
            )values (%s,%s,%s,%s,%s,%s,%s,0,0)
        """, (imagen, nombre_empresa, contacto, direccion, email, password, descripcion,))
    db.commit()
def obtenerEmpresa(id):
    cursor = db.cursor(id)
    cursor.execute("select * from empresa where id_empresa =  %s",(id,))
    obtenerEmpresa = cursor.fetchone()
    return obtenerEmpresa
def cambiar_estado(email):
    cursor = db.cursor()
    cursor.execute("update empresa set estado=1 where email= '"+email+"'")
    db.commit()


def cambiarContraseña(email,password_e):
    cursor = db.cursor()
    cursor.execute("update empresa set contraseña = '"+password_e+"' where email= '"+email+"'")
    db.commit()

def obtenerId(email):
    cursor = db.cursor()
    cursor.execute("select id_empresa from empresa where email = %s", (email+"",))
    obtenerId = cursor.fetchone()
    return obtenerId
def obtenerCategoria(nombreCategoria,id):
    cursor = db.cursor()
    cursor.execute("select * from categoria where nombre = %s and empresa_id = %s",(nombreCategoria, id,))
    nombreCategoria = cursor.fetchone()
    return nombreCategoria

def crearCategoria(id,nombreCategoria):
    cursor = db.cursor()
    cursor.execute("""insert into categoria(
                empresa_id, 
                nombre
            )values (%s,%s)""", (id, nombreCategoria,))
    db.commit()

def listarCategoria(id):
    cursor = db.cursor()
    cursor.execute("select * from categoria where empresa_id=%s",(id,))
    categorias = cursor.fetchall()
    return categorias
def eliminarCategoria(id):
        cursor = db.cursor()
        cursor.execute("delete from categoria where id = %s", (id,))
        db.commit()
def crearProducto(idEmpresa, categoria, disponibilidad,  nombre, precio,imagen, descripcion):
    cursor = db.cursor()
    cursor.execute("""insert into producto(
                id_empresa,
                id_categoria,
                id_estado,
                nombre_producto,
                precio,
                imagen,
                descripcion
            )values (%s,%s,%s,%s,%s,%s,%s)
        """, (idEmpresa+"", categoria, disponibilidad, nombre, precio, imagen,descripcion,))
    db.commit()
def listarProductos(id):
    cursor = db.cursor()
    cursor.execute("""SELECT `producto`.`id_producto`, `imagen`, `nombre_producto`, `categoria`.`nombre`, `precio`, `estado`.`estado`
	FROM `producto`
	INNER JOIN `categoria` ON `producto`.`id_categoria` = `categoria`.`id`
	INNER JOIN `estado`ON `producto`.`id_estado` = `estado`.`id`
	WHERE id_empresa = %s
	GROUP BY `producto`.`id_producto`""", (id,))
    productos = cursor.fetchall()
    return productos
def eliminarProducto(id):
    cursor = db.cursor()
    cursor.execute("delete from producto where id_producto = %s", (id,))
    db.commit()
def obtenerEstado():
    cursor = db.cursor()
    cursor.execute("select * from estado")
    estado = cursor.fetchall()
    return estado
def editarProducto(id):
    cursor = db.cursor()
    cursor.execute("""SELECT `producto`.`id_producto`, `imagen`, `nombre_producto`, `categoria`.`nombre`, `precio`, `estado`.`estado`, `descripcion`
	FROM `producto`
	INNER JOIN `categoria` ON `producto`.`id_categoria` = `categoria`.`id`
	INNER JOIN `estado`ON `producto`.`id_estado` = `estado`.`id`
	WHERE id_producto = %s
	GROUP BY `producto`.`id_producto`""", (id,)) 
    editarProducto=cursor.fetchone()
    return editarProducto

def editarProductosCargar(categoria ,disponibilidad, nombre, precio, imagenn, id, descripcion):
    categoria_sql=''
    disponibilidad_sql=''
    imagen_sql=''
    if imagenn:
        imagen_sql=", imagen= '"+imagenn+"'"
        a = " nombre_producto = '"+nombre+"', precio = '"+precio+"'" + imagen_sql + ", descripcion = '"+descripcion+"' WHERE id_producto = '"+id+"'"
    elif imagenn is None:
        a = " nombre_producto = '"+nombre+"', precio = '"+precio+"'" + imagen_sql + ", descripcion = '"+descripcion+"' WHERE id_producto = '"+id+"'"
    cursor = db.cursor()
    if disponibilidad is not None and categoria is not None:
        disponibilidad_sql = " id_estado = '"+disponibilidad+"',"
        categoria_sql= " id_categoria = '"+categoria+"',"
    elif disponibilidad is not None and categoria is None:
        disponibilidad_sql = " id_estado = '"+disponibilidad+"',"
    if categoria is not None:
        categoria_sql= " id_categoria = '"+categoria+"',"
    
    cursor.execute("UPDATE producto SET " + categoria_sql + disponibilidad_sql + a)
    db.commit()
def verificarCategoriaProducto(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM producto WHERE id_categoria = '"+id+"'")
    producto = cursor.fetchall()
    return producto

def editarEmpresa(imagenn,name,phone,address,password,description,id):
    imagen_sql=''
    password_sql=''
    if password:
        password_sql=" contraseña= '"+password+"', "
    if imagenn:
        imagen_sql=" imagen= '"+imagenn+"', "
    cursor = db.cursor()
    cursor.execute("UPDATE empresa set "+imagen_sql + " nombre_empresa = '"+name+"', contacto = '"+phone+"', direccion = '"+address+"', "+password_sql + "descripcion = '"+description + "' where id_empresa ='"+id+"' ")
    db.commit()

def obtenerProductos(id):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM producto WHERE id_empresa = %s", (id,))
    productos = cursor.fetchall()
    return productos
def listarEmpresas():
    cursor = db.cursor()
    cursor.execute("SELECT * from empresa")
    empresas = cursor.fetchall()
    return empresas
def listarProductosEmpresa(id):
    cursor = db.cursor()
    cursor.execute("SELECT * from producto where id_empresa = %s",(id,))
    empresas = cursor.fetchall()
    return empresas
    