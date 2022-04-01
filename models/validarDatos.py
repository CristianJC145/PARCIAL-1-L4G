def contraseñaValidacion(password): 
      
    SpecialSym =['$', '@', '#', '%'] 
    val = True
      
    if len(password) < 8: 
        print('El tamaño de la contraseña debe ser de minimo 8 caracteres') 
        val = False
          
    if len(password) > 20: 
        print('El tamaño de la contraseña debe ser de maximo 20 caracteres') 
        val = False
          
    if not any(char.isdigit() for char in password): 
        print('La contraseña debe contener numeros') 
        val = False
          
    if not any(char.isupper() for char in password): 
        print('La contraseña debe tener letras mayusculas') 
        val = False
          
    if not any(char.islower() for char in password): 
        print('La contraseña debe tener letras minusculas') 
        val = False
          
    if not any(char in SpecialSym for char in password): 
        print('La contraseña debe tener caracteres especiales') 
        val = False
        
    if val: 
        return val