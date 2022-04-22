from flask import flash


def contraseñaValidacion(password): 
      
    SpecialSym =['$', '@', '#', '%'] 
    val = True
      
    if len(password) < 8:
        flash('El tamaño de la contraseña debe ser de minimo 8 caracteres', 'error') 
        val = False
          
    if len(password) > 20: 
        flash('El tamaño de la contraseña debe ser de maximo 20 caracteres', 'error') 
        val = False
          
    if not any(char.isdigit() for char in password): 
        flash('La contraseña debe contener numeros', 'error') 
        val = False
          
    if not any(char.isupper() for char in password): 
        flash('La contraseña debe tener letras mayusculas', 'error') 
        val = False
          
    if not any(char.islower() for char in password): 
        flash('La contraseña debe tener letras minusculas', 'error') 
        val = False
          
    if not any(char in SpecialSym for char in password): 
        flash('La contraseña debe tener caracteres especiales', 'error') 
        val = False
        
    if val: 
        return val