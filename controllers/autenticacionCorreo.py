from smtplib import SMTP
from email.message import EmailMessage
from config import settings

def enviarEmail(email,link):
    msg = EmailMessage()


    msg.set_content('Para confirmar tu correo ingresa al siguiente link {}'.format(link))
    msg['Subject'] = 'CONFIRMAR CORREO'
    msg['From'] = "cristianjamioy2020@itp.edu.co"
    msg['To'] = email

    username =settings.MAIL_USERNAME
    password =settings.MAIL_PASSWORD

    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.send_message(msg)

    server.quit()
    
def emailBienvenida(email):
    msg = EmailMessage()
    msg.set_content("Bienvenido \n Su cuenta ha sido creada correctamente")
    msg['Subject'] = 'Se ha creado su cuenta'
    msg['From'] = "cristianjamioy2020@itp.edu.co"
    msg['To'] = email

    username =settings.MAIL_USERNAME
    password =settings.MAIL_PASSWORD

    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.send_message(msg)

def emailRecuperacionContraseña(email, link):
    msg = EmailMessage()
    msg.set_content("Usted a solicitado reestablecer su contraseña \nIngrese al siguiente link para continuar con el proceso {}".format(link))
    msg['Subject'] = 'Solicitud de restablecimiento de contraseña'
    msg['From'] = "cristianjamioy2020@itp.edu.co"
    msg['To'] = email

    username =settings.MAIL_USERNAME
    password =settings.MAIL_PASSWORD

    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.send_message(msg)