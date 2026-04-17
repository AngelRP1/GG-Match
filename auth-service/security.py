from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException
from jwt.exceptions import InvalidTokenError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = "firma_secreta_de_ggmatch_super_segura" 
ALGORITHM = "HS256"
MINUTOS_EXPIRACION = 120

def crear_token_acceso(datos: dict):
    # Hacemos una copia de los datos (ej. el username)
    a_encriptar = datos.copy()
    # Le sumamos 2 horas a la hora actual
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    a_encriptar.update({"exp": expiracion})
    
    # Fabricamos el token con nuestra firma secreta
    token_jwt = jwt.encode(a_encriptar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verificar_token_acceso(token: str):
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise excepcion_credenciales
        
        return username 
    
    except InvalidTokenError:
        raise excepcion_credenciales