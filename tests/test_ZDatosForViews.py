from src.modelo.Gasto import Gasto
from src.modelo.Actividad import Actividad
from src.modelo.Viajero import Viajero, ActividadViajero
from src.modelo.declarative_base import engine, Base, Session
import datetime
import unittest

__author__ = "Johan Carvajal"
__copyright__ = "Johan Carvajal"
__license__ = "mit"

class test_ZDatosForViews(unittest.TestCase):


    def test_DatosCargados(self):
        try:
            Base.metadata.create_all(engine)
            '''Abre la sesión'''
            self.session = Session()

            busquedaG = self.session.query(Gasto).all()
            for Act in busquedaG:
                self.session.delete(Act)
            self.session.commit()

            busquedaAV = self.session.query(ActividadViajero).all()
            for Act in busquedaAV:
                self.session.delete(Act)
            self.session.commit()

            busquedaA = self.session.query(Actividad).all()
            for Act in busquedaA:
                self.session.delete(Act)
            self.session.commit()
            busquedaV = self.session.query(Viajero).all()
            for Act in busquedaV:
                self.session.delete(Act)
            self.session.commit()

            Actividad1 = Actividad(nombre="acti 1", terminada=False)

            Actividad2 = Actividad(nombre="acti 2 ", terminada=False)
            Actividad3 = Actividad(nombre="acti 3", terminada=False)
            Viajero1 = Viajero(nombre="pepe", apellido="reyes")
            Viajero2 = Viajero(nombre="ana", apellido="salazar")
            Viajero3 = Viajero(nombre="pedro", apellido="ruiz")
            Viajero4 = Viajero(nombre="luis", apellido="leon")
            Viajero5 = Viajero(nombre="mateo", apellido="rodriguez")

            Gasto1 = Gasto(concepto="Test_Gasto_1", valor=100, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),
                           actividad_Id=2, viajero_Id=1)
            Gasto2 = Gasto(concepto="Test_Gasto_2", valor=500, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),
                           actividad_Id=2, viajero_Id=2)
            Gasto3 = Gasto(concepto="Test_Gasto_3", valor=500, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),
                           actividad_Id=2, viajero_Id=2)
            Gasto4 = Gasto(concepto="Test_Gasto_4", valor=500, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),
                           actividad_Id=2, viajero_Id=3)
            Gasto5 = Gasto(concepto="Test_Gasto_5", valor=100, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),
                           actividad_Id=3, viajero_Id=5)

            ActiViajero1 = ActividadViajero(actividad_id=2, viajero_id=1)
            ActiViajero2 = ActividadViajero(actividad_id=2, viajero_id=2)
            ActiViajero3 = ActividadViajero(actividad_id=2, viajero_id=3)
            ActiViajero4 = ActividadViajero(actividad_id=2, viajero_id=4)

            ActiViajero5 = ActividadViajero(actividad_id=3, viajero_id=5)

            # listaGastos = [["", "pepe reyes", "ana salazar", "pedro ruiz", "luis leon"],
            #                ["pepe reyes", -1, 1200, 1000, 100],
            #                ["ana salazar", 0, -1, 1000, 100], ["pedro ruiz", 0, 0, -1, 0], ["luis leon", 0, 0, -1, 0]]
            #
            self.session.add(Actividad1)

            self.session.add(Actividad2)
            self.session.add(Actividad3)
            self.session.add(Viajero1)
            self.session.add(Viajero2)
            self.session.add(Viajero3)
            self.session.add(Viajero4)
            self.session.add(Viajero5)
            self.session.add(Gasto1)
            self.session.add(Gasto2)
            self.session.add(Gasto3)
            self.session.add(Gasto4)
            self.session.add(Gasto5)

            self.session.add(ActiViajero1)
            self.session.add(ActiViajero2)
            self.session.add(ActiViajero3)
            self.session.add(ActiViajero4)
            self.session.add(ActiViajero5)

            self.session.commit()
            self.session.close()
            self.assertTrue(True)
        except:

            self.assertTrue(False)


