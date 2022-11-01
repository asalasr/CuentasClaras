import datetime

from src.modelo.Gasto import Gasto
from src.modelo.Actividad import Actividad
from src.modelo.Viajero import Viajero, ActividadViajero
from src.logica.Logica_mock import Logica_mock
from src.modelo.declarative_base import engine, Base, Session
from faker import Faker
import unittest

__author__ = "Andres Salas"
__copyright__ = "Andres Salas"
__license__ = "mit"

class test_Actividades(unittest.TestCase):

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

        '''Crea una isntancia de Faker'''
        self.data_factory = Faker()
        '''Se programa para que Faker cree los mismos datos cuando se ejecuta'''
        Faker.seed(1000)

        self.data = []
        self.actividades = []
        self.actividadesTest=[]

        for i in range(0, 10):
            self.data.append((
                self.data_factory.unique.color_name(),
                self.data_factory.boolean()))

            self.actividades.append(
                Actividad(
                    nombre=self.data[-1][0],
                    terminada=self.data[-1][1]
                ))
            self.session.add(self.actividades[-1])

            self.actividadesTest.append(self.actividades[-1])

        '''Persiste los objetos y cierra la sesión'''
        self.session.commit()

    def test_ListarActividades(self):
        listaActividades = Logica_mock.darActividades(self)
        cont = 0

        for act in listaActividades:
            for act_tmp in self.actividadesTest:
                if act["nombre"] == act_tmp.nombre:
                    cont = cont + 1
        self.assertEquals(cont,len(self.actividadesTest))

    def test_ListarActividadesOrdenAlfabetico(self):
        listaActividades = Logica_mock.darActividades(self)
        listaActividades2 = []
        for act in listaActividades:
            listaActividades2.append(act["nombre"])

        for i in range(len(listaActividades2)-1):
            self.assertGreaterEqual(listaActividades2[i+1],listaActividades2[i])

    def test_ListarActividadesVacio(self):
        busqueda = self.session.query(Actividad).all()
        for Act in busqueda:
            self.session.delete(Act)
        self.session.commit()
        self.session.close()

        listaActividades = Logica_mock.darActividades(self)
        self.assertIsNone(listaActividades)

    def test_crearActividad(self):

        ActividadNew = self.data_factory.unique.color_name()

        resp = Logica_mock.crearActividad(self, ActividadNew)
        self.assertTrue(resp)

        '''se valida que si se haya insertado la actividad'''
        listaActividades = Logica_mock.darActividades(self)
        cont = 0
        for act in listaActividades:
            if act["nombre"] == ActividadNew:
                cont = cont + 1
        self.assertGreaterEqual(cont,1)

    def test_eliminarActividadCorrecto(self):
        try:
            eliminada = Logica_mock.eliminarActividad(self,9)
            #actividad correcta
            self.assertTrue(eliminada)
        except:
            self.assertTrue(False)

    def test_elimarActividadConGastos(self):
        try:
            self.session = Session()
            Gasto1 = Gasto(concepto="Test_Gasto_actividad", valor=2000, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"),
                           actividad_Id=1, viajero_Id=1)

            self.session.add(Gasto1)
            self.session.commit()
            self.session.close()

            eliminada = Logica_mock.eliminarActividad(self, 1)
            self.assertFalse(eliminada)
        except:
            self.assertTrue(False)

    def test_elimarActividadBasedeDatos(self):
        try:
            self.session = Session()
            eliminada = Logica_mock.eliminarActividad(self, 8)
            ListaActividad = self.session.query(Actividad).filter(Actividad.id == 8).all()
            self.session.close()
            for lista in ListaActividad:
                self.assertTrue(False)
            self.assertTrue(eliminada)
        except:
            self.assertTrue(False)

    def test_editarActividadExiste(self):
        try:
            editarAct = Logica_mock.editarActividad(self, 1,"actividad1")
            self.assertTrue(editarAct)
        except:
            self.assertTrue(False)

    def test_editarActividadNombreVacio(self):
        try:
            editarViajero, mensaje = Logica_mock.editarActividad(self, 1,"")
            self.assertFalse(editarViajero)

        except:
            self.assertTrue(False)

    def test_editarActividadNombreUnico(self):
        try:
            nameAct = self.data_factory.unique.first_name()
            crearActividad = Logica_mock.crearActividad(self,nameAct)
            self.assertTrue(crearActividad)

            editarActividad, mensaje = Logica_mock.editarActividad(self, 1,nameAct)
            self.assertFalse(editarActividad)
        except:
            self.assertTrue(False)

    def test_editarActividadValidarCambioBase(self):
        try:
            nameAct = self.data_factory.unique.first_name()

            listaActividades = Logica_mock.darActividades(self)

            editarActividad, mensaje = Logica_mock.editarActividad(self, listaActividades[0]["id"],nameAct)

            listaActividades2 = Logica_mock.darActividades(self)

            for act in listaActividades2:
                if act["id"] == listaActividades[0]["id"] and act["nombre"] == nameAct:
                    self.assertTrue(True)

        except:
            self.assertTrue(False)

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Borra todas las Actividades'''
        busqueda = self.session.query(Gasto).all()
        for Act in busqueda:
            self.session.delete(Act)

        busqueda = self.session.query(Actividad).all()
        for Act in busqueda:
            self.session.delete(Act)

        self.session.commit()
        self.session.close()
