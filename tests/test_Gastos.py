from src.modelo.Gasto import Gasto
from src.modelo.Actividad import Actividad
from src.modelo.Viajero import Viajero, ActividadViajero
from src.logica.Logica_mock import Logica_mock
from src.modelo.declarative_base import engine, Base, Session
import datetime
import unittest
from faker import Faker

__author__ = "Johan Carvajal"
__copyright__ = "Johan Carvajal"
__license__ = "mit"

class test_Gastos(unittest.TestCase):

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
        self.data = []
        self.actividades = []
        self.actividadesTest = []

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
        first_name = self.data_factory.unique.first_name()
        last_name = self.data_factory.unique.last_name()
        first_name2 = self.data_factory.unique.first_name()
        last_name2 = self.data_factory.unique.last_name()
        first_name3 = self.data_factory.unique.first_name()
        last_name3 = self.data_factory.unique.last_name()
        first_name4 = self.data_factory.unique.first_name()
        last_name4 = self.data_factory.unique.last_name()
        viajero = []
        viajero.append(
            Viajero(
                nombre=first_name,
                apellido=last_name
            ))
        viajero.append(
            Viajero(
                nombre=first_name2,
                apellido=last_name2
            ))
        viajero.append(
            Viajero(
                nombre=first_name3,
                apellido=last_name3
            ))
        viajero.append(
            Viajero(
                nombre=first_name4,
                apellido=last_name4
            ))
        self.session.add(viajero[0])
        self.session.add(viajero[1])
        self.session.add(viajero[2])
        self.session.add(viajero[3])
        self.session.commit()

        Gasto1 = Gasto(concepto="Test_Gasto_1", valor=2000, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"), actividad_Id=1, viajero_Id=1)
        Gasto2 = Gasto(concepto="Test_Gasto_2", valor=3000, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"), actividad_Id=1, viajero_Id=2)
        Gasto3 = Gasto(concepto="Test_Gasto_3", valor=1000, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"), actividad_Id=1, viajero_Id=2)
        Gasto4 = Gasto(concepto="Test_Gasto_4", valor=1000, fecha=datetime.datetime.strptime("21/12/2008", "%d/%m/%Y"), actividad_Id=2, viajero_Id=3)

        self.session.add(Gasto1)
        self.session.add(Gasto2)
        self.session.add(Gasto3)
        self.session.add(Gasto4)

        '''Persiste los objetos y cierra la sesión'''
        self.session.commit()
        self.session.close()

    def test_listarGastosEnActividadVacia(self):
        listaGastos = Logica_mock.darGastosPorViajeroEnActividad(self,3)
        self.assertIsNone(listaGastos)

    def test_listarGastosVerificarExistenciaCampos(self):
        listaGastos = Logica_mock.darGastosPorViajeroEnActividad(self,2)

        try:
            for act in listaGastos:
                id = act["id"]
                concepto = act["concepto"]
                valor = act["valor"]
                fecha = act["fecha"]
                id_actividad = act["actividad_Id"]
                viajeroName = act["viajero"]
                if concepto == None or valor == None or fecha == None or id_actividad == None or viajeroName == None:
                    self.assertTrue(False)
        except:

            self.assertTrue(False)

        self.assertTrue(True)

    def test_listarGastosVerificarFormatos(self):
        listaGastos = Logica_mock.darGastosPorViajeroEnActividad(self,2)

        try:
            for act in listaGastos:
                id = act["id"]
                concepto = act["concepto"]
                valor = act["valor"]
                fecha = act["fecha"]
                id_actividad = act["actividad_Id"]
                viajeroName = act["viajero"]
                if type(id) != int or type(concepto) != str or type(valor) != float or str != type(fecha) or type(id_actividad) != int or str != type(viajeroName) :
                    self.assertTrue(False)
        except:

            self.assertTrue(False)

        self.assertTrue(True)

    def test_ValidarGastosAsociadosActividad(self):
        listaGastos = Logica_mock.darGastosPorViajeroEnActividad(self,1)

        try:
            for act in listaGastos:
                id_actividad = act["actividad_Id"]
                if id_actividad != 1 :
                    self.assertTrue(False)
        except:

            self.assertTrue(False)

        self.assertTrue(True)


    def test_ValidarGastosOrdenadosPorValor(self):
        listaGastos = Logica_mock.darGastosPorViajeroEnActividad(self,1)
        listaGastos2 = []

        try:

            for act in listaGastos:
                listaGastos2.append(act["valor"])
            print(listaGastos2)
            for i in range(len(listaGastos2) - 1):
                self.assertGreaterEqual(listaGastos2[i], listaGastos2[i+1])
        except:

            self.assertTrue(False)

    def test_creaUnGastoCorrecto(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = self.data_factory.unique.color_name()
            valor = self.data_factory.random_int(min=1000,max=100000)
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self,1,1,concepto,date,valor)
            self.assertTrue(gastoCreado)

        except:
            self.assertTrue(False)


    def test_creaGastoMaximoConcepto(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = "a123456789012345678901234567890"
            valor = self.data_factory.random_int(min=1000,max=100000)
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self,1,1,concepto,date,valor)
            self.assertFalse(gastoCreado)
            concepto = self.data_factory.unique.color_name()
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self, 1, 1, concepto, date, valor)
            self.assertTrue(gastoCreado)
        except:
            self.assertTrue(False)

    def test_creaGastoFechaFormatoIncorrecto(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d/%m/%Y")
            concepto = self.data_factory.unique.color_name()
            valor = self.data_factory.random_int(min=1000,max=100000)
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self,1,1,concepto,date,valor)
            self.assertFalse(gastoCreado)
            date = fecha.strftime("%d-%m-%Y")
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self, 1, 1, concepto, date, valor)
            self.assertTrue(gastoCreado)

        except:
            self.assertTrue(False)

    def test_creaGastoValorMaximo(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = self.data_factory.unique.color_name()
            valor = 9999999999.1
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self,1,1,concepto,date,valor)
            self.assertFalse(gastoCreado)
            valor = 9999999999
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self, 1, 1, concepto, date, valor)
            self.assertTrue(gastoCreado)

        except:
            self.assertTrue(False)

    def test_crearGastoAlmecenarEnBaseDeDatos(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = self.data_factory.unique.color_name()
            valor = self.data_factory.random_int(min=1000,max=100000)
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self,1,3,concepto,date,valor)
            self.assertTrue(gastoCreado)
            self.session = Session()
            ListaGastosActividad = self.session.query(Gasto).filter(Gasto.actividad_Id == 1,Gasto.viajero_Id == 3).all()

            existeGasto = False
            for gasto in ListaGastosActividad:
                if (gasto.concepto == concepto and gasto.valor == valor and gasto.fecha.strftime("%d-%m-%Y") == date ):
                        self.assertTrue(True)
                        existeGasto = True
                else:
                        self.assertTrue(False)

            self.assertTrue(existeGasto)

        except:
            self.assertTrue(False)

    def test_editarUnGastoCorrecto(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = self.data_factory.unique.color_name()
            valor = self.data_factory.random_int(min=1000,max=100000)
            gastoEditado = Logica_mock.editarGasto(self,1,concepto,date,valor,1)
            self.assertTrue(gastoEditado)

        except:
            self.assertTrue(False)

    def test_editarGastoValorMaximo(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = self.data_factory.unique.color_name()
            valor = 9999999999.1
            gastoEditado = Logica_mock.editarGasto(self,1,concepto,date,valor,1)
            self.assertFalse(gastoEditado)
            valor = 9999999999
            gastoEditado = Logica_mock.editarGasto(self,1,concepto,date,valor,1)
            self.assertTrue(gastoEditado)

        except:
            self.assertTrue(False)


    def test_editarGastoFechaFormatoIncorrecto(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d/%m/%Y")
            concepto = self.data_factory.unique.color_name()
            valor = self.data_factory.random_int(min=1000,max=100000)
            gastoEditado = Logica_mock.editarGasto(self,1,concepto,date,valor,1)
            self.assertFalse(gastoEditado)
            date = fecha.strftime("%d-%m-%Y")
            gastoEditado = Logica_mock.editarGasto(self,1,concepto,date,valor,1)
            self.assertTrue(gastoEditado)

        except:
            self.assertTrue(False)

    def test_editarGastoMaximoConcepto(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = "a123456789012345678901234567890"
            valor = self.data_factory.random_int(min=1000,max=100000)
            gastoEditado = Logica_mock.editarGasto(self,1,concepto,date,valor,1)
            self.assertFalse(gastoEditado)
            concepto = self.data_factory.unique.color_name()
            gastoEditado = Logica_mock.editarGasto(self, 1,concepto, date, valor,1)
            self.assertTrue(gastoEditado)
        except:
            self.assertTrue(False)

    def test_editarGastoValoresNulos(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = ""
            valor = 0
            gastoEditado = Logica_mock.editarGasto(self,1,concepto,date,valor,1)
            self.assertFalse(gastoEditado)
            concepto = self.data_factory.unique.color_name()
            valor = self.data_factory.random_int(min=1000, max=100000)
            gastoEditado = Logica_mock.editarGasto(self, 1,concepto, date, valor,1)
            self.assertTrue(gastoEditado)
        except:
            self.assertTrue(False)

    def test_crearGastoValoresNulos(self):
        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = ""
            valor = 0
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self,1,3,concepto,date,valor)
            self.assertFalse(gastoCreado)
            concepto = self.data_factory.unique.color_name()
            valor = self.data_factory.random_int(min=1000, max=100000)
            gastoCreado = Logica_mock.adicionarGastoEnActividad(self,1,3,concepto,date,valor)
            self.assertTrue(gastoCreado)
        except:
            self.assertTrue(False)

    def test_editarGastoAlmecenarEnBaseDeDatos(self):

        try:
            date = str(self.data_factory.date())
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            date = fecha.strftime("%d-%m-%Y")
            concepto = self.data_factory.unique.color_name()
            valor = self.data_factory.random_int(min=1000,max=100000)
            gastoCreado = Logica_mock.editarGasto(self,2,concepto,date,valor,4)
            self.assertTrue(gastoCreado)
            self.session = Session()
            ListaGastosActividad = self.session.query(Gasto).filter(Gasto.id == 2).all()

            editoGasto = False
            for gasto in ListaGastosActividad:

                if (gasto.concepto == concepto and gasto.valor == valor and gasto.fecha.strftime("%d-%m-%Y") == date ):
                        self.assertTrue(True)
                        editoGasto = True
                else:
                        self.assertTrue(False)

            self.assertTrue(editoGasto)

        except:
            self.assertTrue(False)


    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Borra todos los datos'''
        busquedaG = self.session.query(Gasto).all()
        for Act in busquedaG:
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