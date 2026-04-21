from fastapi import FastAPI
import redis
import os

app = FastAPI(title="GG-Match: Stats Service", version="1.0")

# Conectamos con Redis (usamos variable de entorno por si acaso)
REDIS_HOST = os.getenv("REDIS_HOST", "redis") # "redis" es el nombre del contenedor por defecto
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# decore_responses=True hace que Redis nos devuelva texto en vez de bytes
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Stats Service con Redis"}

# Sumar 1 visita a un torneo
@app.post("/torneo/{torneo_id}/visita")
def registrar_visita(torneo_id: str):
    # La magia de Redis: 'incr' suma 1 automáticamente y es súper rápido
    visitas = r.incr(f"torneo:{torneo_id}:visitas")
    return {"torneo_id": torneo_id, "visitas_totales": visitas}

# Ver cuántas visitas tiene
@app.get("/torneo/{torneo_id}/visitas")
def obtener_visitas(torneo_id: str):
    visitas = r.get(f"torneo:{torneo_id}:visitas")
    return {"torneo_id": torneo_id, "visitas_totales": int(visitas) if visitas else 0}