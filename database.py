import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Asegura que el directorio 'data/' exista
os.makedirs("data", exist_ok=True)

# Ruta a la base de datos persistente
DATABASE_URL = "sqlite:///./data/database.db"

# Crea el motor
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crea la clase Base para los modelos
Base = declarative_base()

# Crea la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)
