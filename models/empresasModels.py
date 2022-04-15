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
def cambiar_estado(email):
    cursor = db.cursor()
    cursor.execute("update empresa set estado=1 where email= '"+email+"'")
    db.commit()
def delete_regiters(email):
    cursor = db.cursor()
    cursor.execute("delete from empresa where email != %s and estado!=1", (email,))
    db.commit()
def cambiarContraseña(email,password_e):
    cursor = db.cursor()
    cursor.execute("update empresa set contraseña = '"+password_e+"' where email= '"+email+"'")
    db.commit()
