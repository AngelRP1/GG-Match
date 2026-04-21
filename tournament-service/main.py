from fastapi import FastAPI

app = FastAPI(title="GG-Match: Tournament Service", version="1.0")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Tournament Service corriendo al 100%"}

@app.get("/torneos")
def obtener_torneos():
    # Aquí en el futuro conectaremos a MongoDB para traer brackets reales
    return {
        "torneos": [
            {"id": 1, "nombre": "Torneo Relámpago Smash", "estado": "abierto"},
            {"id": 2, "nombre": "Liga Regional LoL", "estado": "en curso"}
        ]
    }