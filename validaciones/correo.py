import re

def validar_correo(correo):
    """
    Valida que el correo electrónico tenga un formato válido.
    """
    if not isinstance(correo, str):
        return False, "El correo electrónico debe ser una cadena de texto."
    if not re.fullmatch(r'[^@]+@[^@]+\.[a-zA-Z]{2,}', correo):
        return False, "El formato del correo electrónico no es válido."
    return True, ""
