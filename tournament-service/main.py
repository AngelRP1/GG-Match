from fastapi import FastAPI, Body, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os
import jwt

app = FastAPI(title="GG-Match: Tournament Service", version="1.2")

# Configuraciones
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# El secreto DEBE ser exactamente el mismo que usas en tu auth-service
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "firma_secreta_de_ggmatch_super_segura") 
ALGORITHM = "HS256"

client = AsyncIOMotorClient(MONGO_URL)
db = client.ggmatch_db
torneos_collection = db.torneos

security = HTTPBearer()

class Torneo(BaseModel):
    nombre: str
    juego: str
    participantes_max: int
    estado: str = "abierto"

# El Cadenero: Esta función revisa el Gafete (Token)
def validar_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ya expiró, vuelve a hacer login")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Gafete falso o inválido")

@app.get("/")
async def read_root():
    return {"status": "ok", "service": "Tournament Service Protegido"}

# Ruta protegida: Fíjate en el "Depends(validar_token)"
@app.post("/torneos", status_code=201)
async def crear_torneo(torneo: Torneo = Body(...), usuario_valido: dict = Depends(validar_token)):
    nuevo_torneo = await torneos_collection.insert_one(torneo.model_dump()) # Usamos model_dump que es la versión moderna de .dict()
    return {
        "id": str(nuevo_torneo.inserted_id), 
        "message": "Torneo creado con éxito",
        "creado_por": usuario_valido.get("sub") # Extraemos el email o ID de quien lo creó desde el token
    }

# Ruta pública: Cualquiera puede ver los torneos
@app.get("/torneos")
async def listar_torneos():
    torneos = []
    cursor = torneos_collection.find()
    async for documento in cursor:
        documento["_id"] = str(documento["_id"])
        torneos.append(documento)
    return torneos