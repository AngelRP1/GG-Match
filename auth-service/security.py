from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone


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