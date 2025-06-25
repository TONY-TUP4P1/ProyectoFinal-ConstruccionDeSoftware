import re

def validar_contrasena(contrasena):
    """
    Valida que la contraseña tenga al menos 8 caracteres, una mayúscula, una minúscula y un número.
    """
    if not isinstance(contrasena, str):
        return False, "La contraseña debe ser una cadena de texto."
    if len(contrasena) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r'[A-Z]', contrasena):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r'[a-z]', contrasena):
        return False, "La contraseña debe contener al menos una letra minúscula."
    if not re.search(r'\d', contrasena):
        return False, "La contraseña debe contener al menos un número."
    return True, ""
