from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    terminada = Column(Boolean)
    viajeros = relationship('Viajero', secondary='actividad_viajero')
    gastos = relationship('Gasto', cascade='all, delete, delete-orphan')