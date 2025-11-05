# --- validaciones.py ---
# Este módulo contiene funciones reutilizables para
# validar datos de entrada, cumpliendo con los
# requisitos de "Validaciones Estrictas".

def validar_no_vacio(texto):
    """
    Verifica que el texto ingresado no esté vacío o 
    solo contenga espacios en blanco.

    Args:
        texto (str): El string a validar.

    Returns:
        bool: True si el texto es válido (no vacío), False en caso contrario.
    """
    # .strip() elimina espacios al inicio y al final
    # Luego comprobamos si la longitud es mayor a 0
    return len(texto.strip()) > 0

def validar_numero_positivo(numero_str):
    """
    Intenta convertir un string a float y verifica que sea
    un número positivo y mayor a cero.

    Args:
        numero_str (str): El string ingresado por el usuario (ej: "250.50").

    Returns:
        tuple: (True, valor_float) si la validación es exitosa.
            (False, None) si la validación falla (no es número o no es > 0).
    """
    try:
        # 1. Validar el tipo de dato (que sea numérico)
        valor = float(numero_str)
        
        # 2. Validar la lógica de negocio (que sea > 0)
        if valor > 0:
            # ¡CORRECTO! Devuelve DOS valores
            return (True, valor)
        else:
            # Es un número, pero no es positivo (ej: 0 o -5)
            print("Error: El número debe ser mayor a cero.")
            # ¡CORRECTO! Devuelve DOS valores
            return (False, None)
            
    except ValueError:
        # El try...except falla si el valor no se puede
        # convertir a float (ej: "hola" o "")
        print("Error: El valor ingresado no es un número válido.")
        # ¡CORRECTO! Devuelve DOS valores
        return (False, None)