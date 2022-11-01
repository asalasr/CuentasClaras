from src.modelo.Gasto import Gasto
from src.modelo.Actividad import Actividad
from src.modelo.Viajero import Viajero, ActividadViajero
from src.logica.Logica_mock import Logica_mock
from src.modelo.declarative_base import engine, Base, Session
import datetime
import unittest

__author__ = "Andres Salas"
__copyright__ = "Andres Salas"
__license__ = "mit"

class test_ReporteCompensacion(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)
        '''Abre la sesión'''
        self.session = Session()

        '''Borra todos los datos'''
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
        self.session.close()

        Actividad1 = Actividad(nombre="Test_Actividad_1", terminada=False)

        Actividad2 = Actividad(nombre="Test_Actividad_2", terminada=False)
        Actividad3 = Actividad(nombre="Test_Actividad_3", terminada=False)
        Viajero1 = Viajero(nombre="pepe", apellido="reyes")
        Viajero2 = Viajero(nombre="ana", apellido="salazar")
        Viajero3 = Viajero(nombre="pedro", apellido="ruiz")
        Viajero4 = Viajero(nombre="luis", apellido="leon")
        Viajero5 = Viajero(nombre="mateo", apellido="rodriguez")
        Gasto1 = Gasto(concepto="Test_Gasto_1", valor=100, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),actividad_Id=2, viajero_Id=1)
        Gasto2 = Gasto(concepto="Test_Gasto_2", valor=500, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),actividad_Id=2, viajero_Id=2)
        Gasto3 = Gasto(concepto="Test_Gasto_3", valor=500, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),actividad_Id=2, viajero_Id=2)
        Gasto4 = Gasto(concepto="Test_Gasto_4", valor=500, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),actividad_Id=2, viajero_Id=3)
        Gasto5 = Gasto(concepto="Test_Gasto_5", valor=100, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),actividad_Id=3, viajero_Id=5)

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

    def test_ValidarReporteSinGastos(self):
        listaGastos = Logica_mock.generarReporteCompensacion(self, 1)
        self.assertFalse(listaGastos)

    def test_ValidarCabeceraReporte(self):
        listaGastos = Logica_mock.generarReporteCompensacion(self, 2)

        if len(listaGastos[0]) != 5:
            self.assertTrue(False)

        if listaGastos[0][0] != "":
            self.assertTrue(False)

        if not("pepe reyes" in listaGastos[0] and "ana salazar" in listaGastos[0]  and "pedro ruiz" in listaGastos[0]  and "luis leon" in listaGastos[0]):
            self.assertTrue(False)

    def test_ValidarEstructuraMatriz(self):
        listaGastos = Logica_mock.generarReporteCompensacion(self, 2)

        if len(listaGastos)!=5:
            self.assertTrue(False)

        for i in range(len(listaGastos)) :
            if i!=0:
                self.assertEquals(listaGastos[i][i],-1)

            if len(listaGastos[i])!=5:
                self.assertTrue(False)

    def test_ValidarCompensacion(self):
        listaGastos = Logica_mock.generarReporteCompensacion(self, 2)

        listaGastos2 = [["", "pepe reyes", "ana salazar", "pedro ruiz", "luis leon"],
                       ["pepe reyes", -1, 0, 0, 0],
                        ["ana salazar", 300, -1, 0, 300],
                       ["pedro ruiz", 0, 0, -1, 100],
                       ["luis leon", 0, 0, 0, -1]]

        self.assertEquals(listaGastos[0], listaGastos2[0])
        self.assertEquals(listaGastos[1], listaGastos2[1])
        self.assertEquals(listaGastos[2], listaGastos2[2])
        self.assertEquals(listaGastos[3], listaGastos2[3])
        self.assertEquals(listaGastos[4], listaGastos2[4])

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Borra todos los datos'''
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
        self.session.close()