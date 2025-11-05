def validar_no_vacio(texto): #validacion de string con espacios vacios
    #comprobamos si la longitud es mayor a 0
    return len(texto.strip()) > 0



def validar_numeros_enteros(): #solo permite enteros
    try:
        if isinstance(x,str):
            return False
        elif x % 1 == 0:
            return True
        else:
            print (0/0)
    except ZeroDivisionError:
        return False

def validar_numero_positivo(x): #solo permite numeros naturales (1:infinito)
    try:
        if isinstance(x,str):
            return False
        elif x % 1 == 0 and not x <= 0:
            return True
        else:
            print (0/0)
    except ZeroDivisionError:
        return False

def validar_numero_flotante(x):   #valida numeros con decimales
    try:
        if isinstance(x,str):
            return False
        elif x % 1 != 0:
            return True
        else:
            print (0/0)
    except ZeroDivisionError:
        return False


def alta_producto(nombre,precio):  #valida el nombre y precio que debe ser en decimales
    if nombre.isspace():
        return False
    else:
        nombre = True
    if nombre == True:
        if vfloat(precio) == False:
            return False
        else:
            return True


def producto_catidad(nombre,precio):  #valida el nombre y precio que debe ser entero
    if nombre.isspace():
        return False
    else:
        nombre = True
    if nombre == True:
        if vpositivo(precio) == False:
            return False
        else:
            return True

