from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# Creacion de tablas si no existen aun
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GG-Match - Auth & Teams Service",
    version="1.0.0"
)

# Dependencia para conectarse a la BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "online", "mensaje": "Servidor y Base de Datos listos"}

@app.post("/usuarios/")
def crear_usuario_prueba(username: str, email: str, db: Session = Depends(get_db)):
    nuevo_usuario = models.Usuario(username=username, email=email, password_hash="temporal123")
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "¡Usuario creado con éxito!", "datos": nuevo_usuario}