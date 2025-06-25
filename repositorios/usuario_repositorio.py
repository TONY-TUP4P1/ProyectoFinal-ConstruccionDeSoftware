from sqlalchemy.orm import Session
from modelos.usuario import Usuario

def insertar_usuario(session: Session, id, nombre, apellido, correo, contrasena, telefono, fecha_nacimiento):
    nuevo = Usuario(
        id=id,
        nombre=nombre,
        apellido=apellido,
        correo=correo,
        contrasena=contrasena,
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento
    )
    session.add(nuevo)
    session.commit()
    return True

def obtener_usuario_por_correo(session: Session, correo):
    return session.query(Usuario).filter_by(correo=correo).first()

def actualizar_usuario(session: Session, id, **kwargs):
    usuario = session.query(Usuario).filter_by(id=id).first()
    if usuario:
        for clave, valor in kwargs.items():
            setattr(usuario, clave, valor)
        session.commit()

def eliminar_usuario(session: Session, id):
    usuario = session.query(Usuario).filter_by(id=id).first()
    if usuario:
        session.delete(usuario)
        session.commit()

