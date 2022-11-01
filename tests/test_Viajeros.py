from src.modelo.Gasto import Gasto
from src.modelo.Actividad import Actividad
from src.modelo.Viajero import Viajero, ActividadViajero
from src.logica.Logica_mock import Logica_mock
from src.modelo.declarative_base import engine, Base, Session
from faker import Faker
import unittest
import datetime

__author__ = "Johan Carvajal"
__copyright__ = "Johan Carvajal"
__license__ = "mit"


class test_Viajeros(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)
        '''Abre la sesión'''
        self.session = Session()
        self.data_factory = Faker()
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
        self.data_factory = Faker()
        '''Se programa para que Faker cree los mismos datos cuando se ejecuta'''
        Faker.seed(1000)

        self.data = []
        self.actividades = []

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

        self.session.commit()


    def test_llamarCrearViajeroDatosCorrectos(self):
       try:
            first_name = self.data_factory.unique.first_name()
            last_name = self.data_factory.unique.last_name()

            crearViajero, mensaje = Logica_mock.crearViajero(self,first_name,last_name)
            print(mensaje)
            self.assertTrue(crearViajero)
       except :
           self.assertTrue(False)


    def test_verificarEnBaseDeDatos(self):
       try:
            encontrado = False
            first_name = self.data_factory.unique.first_name()
            last_name = self.data_factory.unique.last_name()

            crearViajero, mensaje = Logica_mock.crearViajero(self,first_name,last_name)
            self.assertTrue(crearViajero)
            self.session = Session()
            viajero = self.session.query(Viajero).filter(Viajero.nombre==first_name).all()
            for v in viajero:
                    encontrado = True
            if (encontrado) :
                self.assertTrue(True)
            else:
                self.assertTrue(False)
       except :
           self.assertTrue(False)

    def test_crerViajeroConMaximoNumCaracter(self):
       try:
            crearViajero, mensaje = Logica_mock.crearViajero(self,'1234567890123456','1234567890123456')
            self.assertFalse(crearViajero)
       except :
           self.assertTrue(False)

    def test_crerViajeroDuplicado(self):
       try:
            first_name = self.data_factory.unique.first_name()
            last_name = self.data_factory.unique.last_name()
            crearViajero, mensaje = Logica_mock.crearViajero(self,first_name,last_name)
            self.assertTrue(crearViajero)
            crearViajero, mensaje = Logica_mock.crearViajero(self, first_name, last_name)
            self.assertFalse(crearViajero)

       except :
           self.assertTrue(False)

    def test_crerViajeroDatosIncompletos(self):
       try:
            first_name = self.data_factory.unique.first_name()
            last_name = self.data_factory.unique.last_name()
            crearViajero, mensaje = Logica_mock.crearViajero(self,first_name,'')
            self.assertFalse(crearViajero)
            crearViajero, mensaje = Logica_mock.crearViajero(self, '', last_name)
            self.assertFalse(crearViajero)

       except :
           self.assertTrue(False)


    def test_mensajesDeError(self):
       try:
            first_name = self.data_factory.unique.first_name()
            last_name = self.data_factory.unique.last_name()
            crearViajero, mensaje = Logica_mock.crearViajero(self,first_name,last_name)
            self.assertTrue(crearViajero)
            self.assertTrue(mensaje == '')
            crearViajero, mensaje = Logica_mock.crearViajero(self, first_name, last_name)
            self.assertFalse(crearViajero)
            self.assertTrue(mensaje == 'Este viajero ya existe')
            crearViajero, mensaje = Logica_mock.crearViajero(self, first_name, '')
            self.assertFalse(crearViajero)
            self.assertTrue(mensaje == 'No deben existir datos vacios')
            crearViajero, mensaje = Logica_mock.crearViajero(self, 'nombre otro mas de 15', last_name)
            self.assertFalse(crearViajero)
            self.assertTrue(mensaje == 'Los dos campos deben ser de menos de 15 caracteres')

       except :
           self.assertTrue(False)

    def test_validarSinViajerosPorActividad(self):
        '''Abre la sesión'''
        self.session = Session()
        busqueda = self.session.query(Viajero).all()
        for Act in busqueda:
            self.session.delete(Act)
        self.session.commit()

        try:
            Viajeros = Logica_mock.darViajerosPorActividad(self,1)
            self.assertIsNone(Viajeros)

        except:
            self.assertTrue(False)


    def test_validarObtenerViajeros(self):
        self.session = Session()
        busqueda = self.session.query(Viajero).all()
        for Act in busqueda:
            self.session.delete(Act)
        self.session.commit()
        first_name = self.data_factory.unique.first_name()
        last_name = self.data_factory.unique.last_name()

        viajero=[]
        viajero.append(
            Viajero(
                nombre=first_name,
                apellido=last_name
            ))
        self.session.add(viajero[0])
        self.session.commit()
        Viajeros = Logica_mock.darViajerosPorActividad(self, 1)

        self.assertEquals(1,len(Viajeros))

    def test_validarAsignadosActividad(self):
        self.session = Session()
        busqueda = self.session.query(Viajero).all()
        for Act in busqueda:
            self.session.delete(Act)
        self.session.commit()
        self.session.close()
        self.session = Session()
        first_name = self.data_factory.unique.first_name()
        last_name = self.data_factory.unique.last_name()
        first_name2 = self.data_factory.unique.first_name()
        last_name2 = self.data_factory.unique.last_name()
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
        self.session.add(viajero[0])
        self.session.add(viajero[1])
        self.session.commit()

        ActViajero = []
        ActViajero.append(
            ActividadViajero(
                actividad_id=1,
                viajero_id=1
            ))
        self.session.add(ActViajero[0])
        self.session.commit()
        self.session.close()
        Viajeros = Logica_mock.darViajerosPorActividad(self, 1)

        for v in Viajeros:
            if (first_name +" " + last_name == v["Nombre"]):
                self.assertEquals(True,v["Presente"])
            else:
                self.assertEquals(False, v["Presente"])

    def test_validarActualizarEstadoAsignadViajero(self):

        self.session = Session()
        busqueda = self.session.query(Viajero).all()
        for Act in busqueda:
            self.session.delete(Act)

        self.session.commit()
        self.session.close()

        self.session = Session()
        first_name = self.data_factory.unique.first_name()
        last_name = self.data_factory.unique.last_name()
        first_name2 = self.data_factory.unique.first_name()
        last_name2 = self.data_factory.unique.last_name()
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
        self.session.add(viajero[0])
        self.session.add(viajero[1])
        self.session.commit()

        ActViajero = []
        ActViajero.append(
            ActividadViajero(
                actividad_id=1,
                viajero_id=1
            ))
        self.session.add(ActViajero[0])
        self.session.commit()
        self.session.close()
        Viajeros = Logica_mock.darViajerosPorActividad(self, 1)

        for v in Viajeros:
            if (v["Presente"] == False ):
                v["Presente"] = True
            else:
                v["Presente"] = False

        try:
            Logica_mock.incluirViajeroEnActividad(self,Viajeros,1)
            '''Se valida que se haya actualizado'''
            Viajeros = Logica_mock.darViajerosPorActividad(self, 1)
            for v in Viajeros:
                if (first_name + " " + last_name == v["Nombre"]):
                    self.assertEquals(False, v["Presente"])
                else:
                    self.assertEquals(True, v["Presente"])

        except:
            self.assertTrue(False)


    def test_validarDesvincularViajeroActividadConGasto(self):
        self.session = Session()

        first_name = self.data_factory.unique.first_name()
        last_name = self.data_factory.unique.last_name()

        concepto = self.data_factory.unique.color_name()
        valor = self.data_factory.building_number()

        date =  str(self.data_factory.date())
        date2= datetime.datetime.strptime(date, "%Y-%m-%d")

        viajero = []
        viajero.append(
            Viajero(
                nombre=first_name,
                apellido=last_name
            ))
        self.session.add(viajero[0])

        ActViajero = []
        ActViajero.append(
            ActividadViajero(
                actividad_id=1,
                viajero_id=1
            ))
        self.session.add(ActViajero[0])

        gasto = []
        gasto.append(
            Gasto(
                concepto=concepto,
                valor=valor,
                fecha=date2,
                actividad_Id= 1,
                viajero_Id= 1
            ))
        self.session.add(gasto[0])

        self.session.commit()
        self.session.close()

        Viajeros = Logica_mock.darViajerosPorActividad(self, 1)

        for v in Viajeros:
            v["Presente"]= False

        Correcto, mensaje=Logica_mock.incluirViajeroEnActividad(self, Viajeros, 1)

        self.assertFalse(Correcto)


    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()
        '''Borar actividades viajero'''
        busqueda = self.session.query(ActividadViajero).all()
        for Act in busqueda:
            self.session.delete(Act)
        '''Borar actividades'''
        busqueda = self.session.query(Actividad).all()
        for Act in busqueda:
            self.session.delete(Act)
        '''Borra todos los viajeros'''
        busqueda = self.session.query(Viajero).all()
        for Act in busqueda:
            self.session.delete(Act)

        self.session.commit()
        self.session.close()
