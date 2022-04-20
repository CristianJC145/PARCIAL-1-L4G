from datetime import datetime
from datetime import date

def nombreImagen(imagen):
    today = date.today()
    now = datetime.now()
    fecha= str(today)+str(now.hour)+str(now.minute)+str(now.second)
    nombreImagen = imagen.filename
    return str(fecha) +nombreImagen
def obtenerId(session):
    id=str(session['user_id'][0])
    return id
