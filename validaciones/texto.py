def validar_texto_no_vacio(texto, campo_nombre="campo"):
    """
    Valida que un campo de texto no esté vacío y no sea solo espacios.
    """
    if not isinstance(texto, str):
        return False, f"El {campo_nombre} debe ser una cadena de texto."
    if not texto.strip():
        return False, f"El {campo_nombre} no puede estar vacío."
    return True, ""
