from flask import request

def formulario():
    nombre=request.form.get('name')
    contacto=request.form.get('phone')
    direccion = request.form.get('address')
    descripcion=request.form.get('description')

    return{
        'nombre':nombre,
        'contacto':contacto,
        'direccion':direccion,
        'descripcion':descripcion
    }
