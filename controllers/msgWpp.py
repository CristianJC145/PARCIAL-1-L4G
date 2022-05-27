import pywhatkit

def enviarWpp(numero):
    pywhatkit.sendwhatmsg_instantly(numero, "Nueva venta, revisa tu cuenta")