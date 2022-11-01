from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Viajero(Base):
    __tablename__ = 'viajero'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    actividades = relationship('Actividad', secondary='actividad_viajero')
    gastos = relationship('Gasto', cascade='all, delete, delete-orphan')

class ActividadViajero(Base):
    __tablename__ = 'actividad_viajero'
    actividad_id = Column(
        Integer,
        ForeignKey('actividad.id'),
        primary_key=True)

    viajero_id = Column(
        Integer,
        ForeignKey('viajero.id'),
        primary_key=True)
