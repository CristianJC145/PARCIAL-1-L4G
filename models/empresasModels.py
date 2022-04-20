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
def obtenerCategoria(nombreCategoria):
    cursor = db.cursor()
    cursor.execute("select * from categoria where nombre = %s",(nombreCategoria,))
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
def crearProducto(idEmpresa, categoria, disponibilidad,  nombre, precio,imagen):
    cursor = db.cursor()
    cursor.execute("""insert into producto(
                id_empresa,
                id_categoria,
                id_estado,
                nombre_producto,
                precio,
                imagen
            )values (%s,%s,%s,%s,%s,%s)
        """, (idEmpresa+"", categoria, disponibilidad, nombre, precio, imagen,))
    db.commit()
def listarProductos(ids):
    cursor = db.cursor()
    cursor.execute("""SELECT `producto`.`id_producto`, `imagen`, `nombre_producto`, `categoria`.`nombre`, `precio`, `estado`.`estado`
	FROM `producto`
	INNER JOIN `categoria` ON `producto`.`id_categoria` = `categoria`.`id`
	INNER JOIN `estado`ON `producto`.`id_estado` = `estado`.`id`
	WHERE id_empresa = %s
	GROUP BY `producto`.`id_producto`""", (ids,))
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
    cursor.execute("""SELECT `producto`.`id_producto`, `imagen`, `nombre_producto`, `categoria`.`nombre`, `precio`, `estado`.`estado`
	FROM `producto`
	INNER JOIN `categoria` ON `producto`.`id_categoria` = `categoria`.`id`
	INNER JOIN `estado`ON `producto`.`id_estado` = `estado`.`id`
	WHERE id_producto = %s
	GROUP BY `producto`.`id_producto`""", (id,)) 
    editarProducto=cursor.fetchone()
    return editarProducto

def editarProductosCargar(categoria ,disponibilidad, nombre, precio, imagenn,id):

    cursor = db.cursor()
    cursor.execute("UPDATE producto SET id_categoria = '"+categoria+"', id_estado = '"+disponibilidad+"', nombre_producto = '"+nombre+"', precio = '"+precio+"', imagen= '"+imagenn+"' WHERE id_producto = '"+id+"'")
    db.commit()

def editarProductosCargar2(nombre, precio,id):
    cursor = db.cursor()
    cursor.execute("UPDATE producto SET nombre_producto = '"+nombre+"', precio = '"+precio+"' WHERE id_producto = '"+id+"'")
    db.commit()