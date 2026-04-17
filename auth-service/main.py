from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas 
import security 
from database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GG-Match - Auth & Teams Service", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "online", "mensaje": "Servidor y Base de Datos listos"}

# --- RUTA ACTUALIZADA ---
@app.post("/usuarios/")
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Encriptamos la contraseña que viene en el molde
    contra_encriptada = security.get_password_hash(usuario.password)
    
    # 2. Creamos el registro para la BD (reemplazando temporal123)
    nuevo_usuario = models.Usuario(
        username=usuario.username, 
        email=usuario.email, 
        password_hash=contra_encriptada
    )
    
    # 3. Guardamos
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {"mensaje": "¡Usuario creado de forma segura!", "datos": nuevo_usuario}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.username == form_data.username).first()
    
    if not usuario_db or not security.verify_password(form_data.password, usuario_db.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_acceso = security.crear_token_acceso(datos={"sub": usuario_db.username})
    
    return {"access_token": token_acceso, "token_type": "bearer"}