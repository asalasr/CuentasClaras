import datetime

from src.modelo.Gasto import Gasto
from src.modelo.Actividad import Actividad
from src.modelo.Viajero import Viajero, ActividadViajero
from src.logica.Logica_mock import Logica_mock
from src.modelo.declarative_base import engine, Base, Session
import unittest
from faker import Faker


__author__ = "Andres Salas"
__copyright__ = "Andres Salas"
__license__ = "mit"

class test_ReporteGastos(unittest.TestCase):

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


        self.data_factory = Faker()
        Faker.seed(1000)




        self.actividades = []

        for i in range(0, 10):
            self.actividades.append(
                Actividad(
                    nombre=self.data_factory.unique.color_name(),
                    terminada=self.data_factory.boolean()
                ))
            self.session.add(self.actividades[-1])
        self.session.commit()
        self.viajeros = []
        self.viajerosTest = []
        for i in range(0, 10):
            first_name = self.data_factory.unique.first_name()
            last_name = self.data_factory.unique.last_name()
            self.viajerosTest.append({"Nombre":first_name,"ValorAct2":0,"ValorAct3":0})
            self.viajeros.append(
                Viajero(
                    nombre=first_name,
                    apellido=last_name
                ))
            self.session.add(self.viajeros[-1])
        self.session.commit()
        self.ActViajero = []
        #Actividad 2 muchos gastos por viajero
        self.ActViajero.append(
            ActividadViajero(
                    actividad_id=2,
                    viajero_id=1,
            ))
        self.ActViajero.append(
            ActividadViajero(
                    actividad_id=2,
                    viajero_id=2,
            ))
        self.ActViajero.append(
            ActividadViajero(
                    actividad_id=2,
                    viajero_id=3,
            ))
        # Actividad 1 sin gastos
        self.ActViajero.append(
            ActividadViajero(
                    actividad_id=1,
                    viajero_id=2,
            ))
        self.ActViajero.append(
            ActividadViajero(
                    actividad_id=1,
                    viajero_id=3,
            ))
        #Actividad 3,  1 gasto por viajero
        self.ActViajero.append(
            ActividadViajero(
                    actividad_id=3,
                    viajero_id=2,
            ))
        self.ActViajero.append(
            ActividadViajero(
                    actividad_id=3,
                    viajero_id=3,
            ))

        for act in self.ActViajero:
            self.session.add(act)


        valor = self.data_factory.random_int(min=1000,max=100000)
        date = str(self.data_factory.date())
        date2 = datetime.datetime.strptime(date, "%Y-%m-%d")
        Gasto1 = Gasto(concepto=self.data_factory.company(), valor=valor, fecha=date2,
                       actividad_Id=3, viajero_Id=3)
        self.viajerosTest[2]["ValorAct3"]=valor
        valor = self.data_factory.random_int(min=1000,max=100000)
        Gasto2 = Gasto(concepto=self.data_factory.company(), valor=valor, fecha=date2,
                       actividad_Id=3, viajero_Id=2)
        self.viajerosTest[1]["ValorAct3"]=valor
        self.session.add(Gasto1)
        self.session.add(Gasto2)
        self.session.commit()

        valor = self.data_factory.random_int(min=1000, max=100000)
        total = valor
        Gasto1 = Gasto(concepto=self.data_factory.company(), valor=valor, fecha=date2,
                       actividad_Id=2, viajero_Id=1)
        valor = self.data_factory.random_int(min=1000, max=100000)
        total = valor+total
        Gasto2 = Gasto(concepto=self.data_factory.company(), valor=valor, fecha=date2,
                       actividad_Id=2, viajero_Id=1)
        self.viajerosTest[0]["ValorAct2"] = total
        self.session.add(Gasto1)
        self.session.add(Gasto2)
        self.session.commit()

        valor = self.data_factory.random_int(min=1000, max=100000)
        total = valor
        Gasto1 = Gasto(concepto=self.data_factory.company(), valor=valor, fecha=date2,
                       actividad_Id=2, viajero_Id=2)
        valor = self.data_factory.random_int(min=1000, max=100000)
        total = valor + total
        Gasto2 = Gasto(concepto=self.data_factory.company(), valor=valor, fecha=date2,
                       actividad_Id=2, viajero_Id=2)
        self.viajerosTest[1]["ValorAct2"] = total
        self.session.add(Gasto1)
        self.session.add(Gasto2)
        self.session.commit()




        self.session.close()

    def test_ValidarReporteGastosSinViajeros(self):
        try:
            listaGastos = Logica_mock.generarReporteGastos(self, 4)
            self.assertEquals([], listaGastos)
        except :
            self.assertTrue(False)

    def test_ValidarReporteGastosSinGastos(self):
        try:

            listaGastos = Logica_mock.generarReporteGastos(self, 1)
            self.assertNotEqual([], listaGastos)

            for gasto in listaGastos:
                if(gasto["Nombre"]==self.viajerosTest[1]["Nombre"] or gasto["Nombre"]==self.viajerosTest[2]["Nombre"]):
                    if gasto["Valor"] != 0:
                        self.assertTrue(False)
                else:
                    self.assertTrue(False)

            self.assertTrue(True)
        except :
            self.assertTrue(False)

    def test_ValidarReporteGastosIndividual(self):
        try:

            listaGastos = Logica_mock.generarReporteGastos(self, 3)
            self.assertNotEqual([], listaGastos)

            for gasto in listaGastos:
                if((gasto["Nombre"]==self.viajerosTest[1]["Nombre"] and gasto["Valor"]==self.viajerosTest[1]["ValorAct3"] )or (gasto["Nombre"]==self.viajerosTest[2]["Nombre"] and gasto["Valor"]==self.viajerosTest[2]["ValorAct3"])):
                        self.assertTrue(True)
                else:
                    self.assertTrue(False)

            self.assertTrue(True)
        except :
            self.assertTrue(False)

    def test_ValidarReporteGastosSuma(self):
        try:

            listaGastos = Logica_mock.generarReporteGastos(self, 2)
            self.assertNotEqual([], listaGastos)

            for gasto in listaGastos:
                if((gasto["Nombre"]==self.viajerosTest[0]["Nombre"] and gasto["Valor"]==self.viajerosTest[0]["ValorAct2"] )
                        or (gasto["Nombre"]==self.viajerosTest[1]["Nombre"] and gasto["Valor"]==self.viajerosTest[1]["ValorAct2"])
                        or (gasto["Nombre"]==self.viajerosTest[2]["Nombre"] and gasto["Valor"]==self.viajerosTest[2]["ValorAct2"])):
                        self.assertTrue(True)
                else:
                    self.assertTrue(False)

            self.assertTrue(True)
        except :
            self.assertTrue(False)

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