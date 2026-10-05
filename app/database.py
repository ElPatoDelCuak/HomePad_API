from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# Motor de conexión a PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para las entidades ORM
class Base(DeclarativeBase):
    pass

# Generador de sesión de DB para Inyección de Dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()