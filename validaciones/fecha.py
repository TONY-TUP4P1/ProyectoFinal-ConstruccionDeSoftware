import datetime

def validar_fecha(fecha):
    """
    Valida que la fecha tenga el formato DD/MM/AAAA y sea una fecha real.
    """
    if not isinstance(fecha, str):
        return False, "La fecha debe ser una cadena de texto."
    try:
        datetime.datetime.strptime(fecha, "%d/%m/%Y")
        return True, ""
    except ValueError:
        return False, "La fecha no tiene un formato válido o no existe (debe ser DD/MM/AAAA)."
