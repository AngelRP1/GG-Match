from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas 
import security 
from database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GG-Match - Auth & Teams Service", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

@app.get("/perfil/mi-info")
def ver_mi_perfil(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    # 1. Le damos el token a seguridad para que lo verifique
    username = security.verificar_token_acceso(token)
    
    # 2. Si pasó la prueba, buscamos sus datos reales en la BD
    usuario = db.query(models.Usuario).filter(models.Usuario.username == username).first()
    
    # 3. Le mostramos su zona VIP (sin revelar el password_hash por seguridad)
    return {
        "mensaje": "¡Bienvenido a la Zona VIP!",
        "datos_usuario": {
            "id": usuario.id,
            "username": usuario.username,
            "email": usuario.email,
            "rol": usuario.rol
        }
    }

# RUTA 1: CREAR UN EQUIPO
@app.post("/equipos/")
def crear_equipo(
    datos_equipo: schemas.EquipoCreate, 
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    # Validamos quién es el usuario logueado
    username = security.verificar_token_acceso(token)
    usuario_db = db.query(models.Usuario).filter(models.Usuario.username == username).first()

    # Creamos el equipo en la BD
    nuevo_equipo = models.Equipo(nombre=datos_equipo.nombre, descripcion=datos_equipo.descripcion)
    db.add(nuevo_equipo)
    db.commit()
    db.refresh(nuevo_equipo)
    
    # Automáticamente, el usuario que lo crea se une al equipo
    usuario_db.equipo_id = nuevo_equipo.id
    db.commit()

    return {"mensaje": f"¡El equipo '{nuevo_equipo.nombre}' ha sido creado!", "equipo": nuevo_equipo}


# RUTA 2: UNIRSE A UN EQUIPO EXISTENTE
@app.post("/equipos/unirse/{equipo_id}")
def unirse_equipo(
    equipo_id: int, 
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    # Validamos al usuario
    username = security.verificar_token_acceso(token)
    usuario_db = db.query(models.Usuario).filter(models.Usuario.username == username).first()

    # Verificamos que el equipo exista
    equipo_db = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if not equipo_db:
        raise HTTPException(status_code=404, detail="El equipo no existe")

    # Asignamos el jugador al equipo
    usuario_db.equipo_id = equipo_db.id
    db.commit()
    db.refresh(usuario_db)

    return {"mensaje": f"¡Te has unido exitosamente al equipo '{equipo_db.nombre}'!"}