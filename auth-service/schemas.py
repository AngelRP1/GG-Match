from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str  # Esta es la contraseña real que escribirá el usuario

class EquipoCreate(BaseModel):
    nombre: str
    descripcion: str = None # La descripción es opcional