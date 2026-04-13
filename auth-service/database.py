from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión al Postgres que está corriendo en Docker
SQLALCHEMY_DATABASE_URL = "postgresql://admin:superpassword123@ggmatch_postgres:5432/auth_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()