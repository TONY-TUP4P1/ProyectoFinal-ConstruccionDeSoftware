"""
database.py

Define la configuración de conexión con la base de datos SQLite y proporciona la sesión local
(SQLAlchemy ORM). También expone la base declarativa (Base) para registrar todos los modelos.

Utiliza:
    - SQLite
    - SQLAlchemy

Funciones:
    get_session() -> Session: Devuelve una nueva sesión de base de datos.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Asegura que el directorio 'data/' exista
os.makedirs("data", exist_ok=True)

# Ruta a la base de datos
DATABASE_URL = "sqlite:///./data/database.db"

# Crea el motor
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base para los modelos
Base = declarative_base()

# Crea la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión


def get_session():
    return SessionLocal()
