from fastapi import FastAPI, Body
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List
import os

app = FastAPI(title="GG-Match: Tournament Service", version="1.1")

# Configuración de MongoDB (Usamos variables de entorno por seguridad)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.ggmatch_db
torneos_collection = db.torneos

# Modelo de datos para validar lo que entra
class Torneo(BaseModel):
    nombre: str
    juego: str
    participantes_max: int
    estado: str = "abierto"

@app.get("/")
async def read_root():
    return {"status": "ok", "service": "Tournament Service con MongoDB"}

@app.post("/torneos", status_code=201)
async def crear_torneo(torneo: Torneo = Body(...)):
    nuevo_torneo = await torneos_collection.insert_one(torneo.dict())
    return {"id": str(nuevo_torneo.inserted_id), "message": "Torneo creado con éxito en Mongo"}

@app.get("/torneos")
async def listar_torneos():
    torneos = []
    cursor = torneos_collection.find()
    async for documento in cursor:
        documento["_id"] = str(documento["_id"]) # Convertir ID de Mongo a texto
        torneos.append(documento)
    return torneos