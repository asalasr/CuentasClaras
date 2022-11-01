from sqlalchemy import desc, func

from src.modelo.declarative_base import engine, Base, Session
from src.modelo.Viajero import Viajero, ActividadViajero
from src.modelo.Actividad import Actividad
from src.modelo.Gasto import Gasto
from datetime import datetime
import tkinter

class Logica_mock():

    def __init__(self):
        # Crea la BD
        Base.metadata.create_all(engine)

        #Este constructor contiene los datos falsos para probar la interfaz
        #self.actividades = ["Actividad 1"]
        self.viajeros = [{"Nombre":"Pepe", "Apellido":"Pérez"}, {"Nombre":"Ana", "Apellido":"Andrade"}]
        self.gastos = [{"Concepto":"Gasto 1", "Fecha": "12-12-2020", "Valor": 10000, "Nombre": "Pepe", "Apellido": "Pérez"}, {"Concepto":"Gasto 2", "Fecha": "12-12-2020", "Valor": 20000, "Nombre":"Ana", "Apellido":"Andrade"}]
        # self.matriz = None
        #self.gastos_consolidados = [{"Nombre":"Pepe", "Apellido":"Pérez", "Valor":15000}, {"Nombre":"Ana", "Apellido":"Andrade", "Valor":12000},{"Nombre":"Pedro", "Apellido":"Navajas", "Valor":0}]

    def darActividades(self):
        actividades = []
        session = Session()
        listactividades = session.query(Actividad).order_by("nombre").all()
        print("llego aca")
        if listactividades == []:
            return None

        for actividad in listactividades:
            actividades.append({"id":actividad.id,"nombre":actividad.nombre, "terminada":actividad.terminada})

        return actividades

    def darGastosPorViajeroEnActividad(self,id_actividad):
        session = Session()

        listagastos = session.query(Gasto).filter(Gasto.actividad_Id==id_actividad).order_by(desc("valor")).all()
        array_gasto=[]

        if listagastos == []:
            return None

        dateTimeObj = datetime.now()

        for gasto in listagastos:
            viajero = session.query(Viajero).filter(Viajero.id==gasto.viajero_Id).all()

            dateTimeObj = gasto.fecha

            for v in viajero:
                array_gasto.append({"id":gasto.id,"concepto":gasto.concepto,"valor":gasto.valor,"fecha":dateTimeObj.strftime("%d-%m-%Y"),"actividad_Id":gasto.actividad_Id,"viajero":v.nombre + " "+ v.apellido})

        return array_gasto

    def generarReporteCompensacion (self,id_actividad):
        session = Session()

        ListaGastosActividad = session.query(Gasto,func.sum(Gasto.valor).label("valor"),(Gasto.viajero_Id).label("viajero_Id")).filter(Gasto.actividad_Id==id_actividad).group_by(Gasto.viajero_Id).all()
        ListaActividadViajero = session.query(ActividadViajero).filter(ActividadViajero.actividad_id == id_actividad).all()


        if ListaGastosActividad == [] or  ListaActividadViajero == []:
            return None

        sumaTotalGastos = 0
        gastoPorPersona= 0
        for gasto in ListaGastosActividad:

            sumaTotalGastos += gasto.valor


        listaViajerosDeuda = []
        listaEncabezados = []
        Matriz_Salida = []

        #Crear encabezados
        listaEncabezados.append("")
        contarNumeroViajeros = 0
        for actividad_viajero in ListaActividadViajero:
            contarNumeroViajeros += 1

        gastoPorPersona = sumaTotalGastos/contarNumeroViajeros
        for actividad_viajero in ListaActividadViajero:
            viajero = session.query(Viajero).filter(Viajero.id == actividad_viajero.viajero_id).all()
            for v in viajero:
                listaEncabezados.append(v.nombre+" "+v.apellido)
                noExiste = True
                for gasto in ListaGastosActividad:
                    if gasto.viajero_Id == v.id:
                        listaViajerosDeuda.append([v.id,v.nombre+" "+v.apellido,gastoPorPersona-gasto.valor])
                        noExiste = False
                if noExiste == True:
                    listaViajerosDeuda.append([v.id,v.nombre+" "+v.apellido,gastoPorPersona])

        Matriz_Salida.append(listaEncabezados)

        #Agregar otros
        listaPorViajero = []
        i = 0
        j =  0
        for i in range(len(listaEncabezados)-1):
            listaPorViajero.append(listaEncabezados[i+1])

            for j in range(len(listaEncabezados)-1):
                if i != j:


                    if (listaViajerosDeuda[i][2] < 0):

                        if listaViajerosDeuda[j][2] > 0:

                            if  listaViajerosDeuda[j][2] >= abs(listaViajerosDeuda[i][2]):
                                listaPorViajero.append(abs(listaViajerosDeuda[i][2]))
                                listaViajerosDeuda[j][2] = listaViajerosDeuda[j][2]-abs(listaViajerosDeuda[i][2])
                                listaViajerosDeuda[i][2] = 0
                            elif listaViajerosDeuda[j][2] <  abs(listaViajerosDeuda[i][2]):
                                listaPorViajero.append(abs(listaViajerosDeuda[i][2])-listaViajerosDeuda[j][2])
                                listaViajerosDeuda[i][2] = listaViajerosDeuda[j][2] + listaViajerosDeuda[i][2]
                                listaViajerosDeuda[j][2] = 0
                        else:
                            listaPorViajero.append(0)
                    else:
                        listaPorViajero.append(0)

                else:
                    listaPorViajero.append(-1)

            Matriz_Salida.append(listaPorViajero[:])
            listaPorViajero.clear()


        #Traer gastos

        return Matriz_Salida


    def crearActividad(self,nombreActividad):
        session = Session()
        try:
            if (nombreActividad == ''):
                return False

            nomActividad = session.query(Actividad).filter(Actividad.nombre == nombreActividad).all()
            for ac in nomActividad:
                return False

            newActividad = Actividad(nombre=nombreActividad, terminada=False)
            session.add(newActividad)
            session.commit()
            session.close()
            return True
        except:
            return False

    def crearViajero(self,nombre,apellido):

         try:
            if(apellido == '' or nombre == ''):
                return False, 'No deben existir datos vacios'
            if (len(nombre) > 15 or len(apellido) > 15):
                return False, 'Los dos campos deben ser de menos de 15 caracteres'

            session = Session()
            encontrado = False

            viajero = session.query(Viajero).filter(Viajero.nombre == nombre,Viajero.apellido == apellido).all()
            if(viajero):
                for v in viajero:
                    encontrado = True
            if not (encontrado):
                Viajero1 = Viajero(nombre=nombre, apellido=apellido)
                session.add(Viajero1)
                session.commit()
                session.close()
                return True, ''

            else:
                return False,'Este viajero ya existe'
         except Exception as e:
             print(e)
             return False, 'Error inesperado'

    def darViajerosPorActividad(self, id_actividad):
        session = Session()
        viajero = session.query(Viajero).all()
        viajeros_lista = []
        if (viajero):
            for v in viajero:
                ListaActividadViajero = session.query(ActividadViajero).filter(ActividadViajero.actividad_id == id_actividad,ActividadViajero.viajero_id == v.id ).all()
                present = False
                for actividad_viajero in ListaActividadViajero:
                    present = True
                viajeros_lista.append({"id":v.id,"Nombre": v.nombre+" "+v.apellido, "Presente":present})
        if (viajeros_lista == []):
            return None
        return viajeros_lista

    def incluirViajeroEnActividad(self, viajeros,id_actividad):
        try:
            session = Session()
            respuesta = True
            mensaje = ''
            if (viajeros == []):
                return True, ''
            if (viajeros):
                for v in viajeros:
                    ListaActividadViajero = session.query(ActividadViajero).filter(ActividadViajero.actividad_id == id_actividad, ActividadViajero.viajero_id == v["id"]).all()
                    present = False
                    AcV = None
                    for actividad_viajero in ListaActividadViajero:
                        AcV = actividad_viajero
                        present = True
                    if(present != v["Presente"]):
                        if(v["Presente"]==True):
                            ActiViajero = ActividadViajero(actividad_id=id_actividad, viajero_id=v["id"])
                            session.add(ActiViajero)

                        else:
                            ListaGastosActividad = session.query(Gasto).filter(Gasto.actividad_Id == id_actividad, Gasto.viajero_Id==v["id"]).all()
                            tieneGasto = False
                            for gasto in ListaGastosActividad:
                                tieneGasto = True
                            if(tieneGasto==False):
                                session.delete(AcV)
                            else:
                                mensaje = mensaje + ' '+v["Nombre"]+','
                                respuesta = False
            session.commit()
            session.close()
            if not (respuesta):
                mensaje+=' tienen gastos asociados'
            return respuesta,mensaje
        except Exception as e:
            print(e)
            return False, str(e)

    def generarReporteGastos (self,id_actividad):
        session = Session()

        ListaActividadViajero = session.query(ActividadViajero).filter(ActividadViajero.actividad_id == id_actividad).all()

        listaViajeros=[]

        for actividad_viajero in ListaActividadViajero:
            viajeros = session.query(Viajero).filter(Viajero.id == actividad_viajero.viajero_id).all()

            for viajero in viajeros:
                #listagastos = session.query(Gasto).filter(Gasto.actividad_Id == id_actividad,Gasto.viajero_Id == viajero.id).all()
                ListaGastosActividad = session.query(Gasto, func.sum(Gasto.valor).label("valor"),(Gasto.viajero_Id).label("viajero_Id")).filter(Gasto.actividad_Id == id_actividad,Gasto.viajero_Id == viajero.id).group_by(Gasto.viajero_Id).all()
                valor = 0
                for gastos in ListaGastosActividad:
                    valor = gastos.valor


                listaViajeros.append({"Nombre": viajero.nombre, "Apellido": viajero.apellido, "Valor": valor})

        return listaViajeros

    def adicionarGastoEnActividad(self, id_actividad, id_viajero, concepto, date, valor):
         try:
            if ((len(concepto) > 30) or not((date.endswith("-", 2, 3) and date.endswith("-", 5, 6))) or (float(valor) > float(9999999999)) or (float(valor) <= 0) or (concepto == "")):

               return False

            else:

                session = Session()
                Gasto1 = Gasto(concepto=concepto, valor=valor,
                               fecha=datetime.strptime(date, "%d-%m-%Y"), actividad_Id=id_actividad, viajero_Id=id_viajero)
                session.add(Gasto1)
                session.commit()
                session.close()
                return True

         except Exception as e:
                print(e)
                return False

    def editarGasto(self,id_gasto,concepto,date,valor,id_viajero):
        try:

            if ((len(concepto) > 30) or not((date.endswith("-", 2, 3) and date.endswith("-", 5, 6))) or (float(valor) > float(9999999999)) or (float(valor) <= 0) or (concepto == "")):
                return False

            else:
                session = Session()
                ListaGastosActividad = session.query(Gasto).filter(Gasto.id == id_gasto).all()
                for gasto in ListaGastosActividad:
                    gasto.concepto = concepto
                    gasto.fecha = datetime.strptime(date, "%d-%m-%Y")
                    gasto.valor = valor
                    gasto.viajero_Id = id_viajero
                    session.add(gasto)
                    session.commit()
                    session.close()
                    return True
                return False
        except Exception as e:
                print(e)
                return False

    def eliminarActividad (self,id_actividad):
        session = Session()
        try:
            ListaGastosActividad = session.query(Gasto).filter(Gasto.actividad_Id == id_actividad).all()

            for gasto in ListaGastosActividad:
                return False

            actViajero = session.query(ActividadViajero).filter(ActividadViajero.actividad_id == id_actividad).all()
            for ac in actViajero:
                session.delete(ac)
            session.commit()

            actividad = session.query(Actividad).filter(Actividad.id == id_actividad).all()
            for ac in actividad:
                session.delete(ac)
            session.commit()

            session.close()

            return True
        except Exception as e:
            return False

    def editarActividad (self,id_actividad,nombre_actividad):
        session = Session()
        if (nombre_actividad == ''):
            return False, 'El nombre de la actividad no debe ser vacio.'

        nombreActividad = session.query(Actividad).filter(Actividad.nombre == nombre_actividad).all()
        for ac in nombreActividad:
            return False, "La actividad ya existe, validar."


        actividad = session.query(Actividad).filter(Actividad.id == id_actividad).all()

        if actividad==None:
            return False,'No existe actividad'

        for act in actividad:
            act.nombre = nombre_actividad
            session.add(act)
            session.commit()
            session.close()
            return True, ''