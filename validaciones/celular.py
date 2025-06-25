import re

def validar_numero_celular(numero):
    """
    Valida que el número de celular contenga exactamente 9 dígitos numéricos.
    """
    if not isinstance(numero, str):
        return False, "El número de celular debe ser una cadena de texto."
    if not re.fullmatch(r'\d{9}', numero):
        return False, "El número de celular debe contener exactamente 9 dígitos numéricos."
    return True, ""
