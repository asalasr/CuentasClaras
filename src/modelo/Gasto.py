from sqlalchemy import Column, Integer, String, ForeignKey,REAL,Date
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Gasto(Base):
    __tablename__ = 'gasto'

    id = Column(Integer, primary_key=True)
    concepto = Column(String)
    valor = Column(REAL)
    fecha = Column(Date)
    actividad_Id = Column(Integer, ForeignKey('actividad.id'))
    viajero_Id = Column(Integer, ForeignKey('viajero.id'))
