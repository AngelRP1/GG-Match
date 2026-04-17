from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String, nullable=True)
    
    # Esta relación nos permite ver a todos los jugadores del equipo fácilmente
    jugadores = relationship("Usuario", back_populates="equipo")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String) 
    rol = Column(String, default="jugador")
    
    # ¡NUEVO! Llave foránea que conecta al usuario con su equipo
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=True)
    
    # Esta relación nos permite acceder al objeto Equipo desde el Usuario
    equipo = relationship("Equipo", back_populates="jugadores")