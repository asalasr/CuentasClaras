from PyQt5.QtWidgets import QApplication
from .Vista_lista_actividades import Vista_lista_actividades
from .Vista_lista_viajeros import Vista_lista_viajeros
from .Vista_actividad import Vista_actividad
from .Vista_reporte_compensacion import Vista_reporte_compensacion
from .Vista_reporte_gastos import Vista_reporte_gastos_viajero
import tkinter
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tkinter import messagebox


class App_CuentasClaras(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_CuentasClaras, self).__init__(sys_argv)
        
        self.logica = logica
        self.mostrar_vista_lista_actividades()
        
        
    def mostrar_vista_lista_actividades(self):
        """
        Esta función inicializa la ventana de la lista de actividades
        """

        self.vista_lista_actividades = Vista_lista_actividades(self)
        self.vista_lista_actividades.mostrar_actividades(self.logica.darActividades())


    def insertar_actividad(self, nombre):
        """
        Esta función inserta una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.crearActividad(nombre)
        self.vista_lista_actividades.mostrar_actividades(self.logica.darActividades())

    def editar_actividad(self, actividad, nombre):
        """
        Esta función editar una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.editarActividad(actividad["id"],nombre)
        self.vista_lista_actividades.mostrar_actividades(self.logica.darActividades())

    def eliminar_actividad(self, indice_actividad):
        """
        Esta función elimina una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        eliminarActividad=self.logica.eliminarActividad(indice_actividad)
        print("llego a eliminar:", eliminarActividad)

        if not (eliminarActividad):

            mensaje_confirmacion = QMessageBox()
            mensaje_confirmacion.setIcon(QMessageBox.Warning)
            mensaje_confirmacion.setText(
                "Actividad no se puede eliminar por gastos asociados")
            mensaje_confirmacion.setWindowTitle("borrar actividad")
            mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
            respuesta = mensaje_confirmacion.exec_()

        self.vista_lista_actividades.mostrar_actividades(self.logica.darActividades())


    def mostrar_viajeros(self):
        """
        Esta función muestra la ventana de la lista de viajeros
        """

        self.vista_lista_viajeros=Vista_lista_viajeros(self)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def insertar_viajero(self, nombre, apellido):
        """
        Esta función inserta un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        susessfull, message = self.logica.crearViajero(nombre,apellido)

        if (susessfull):
            self.logica.viajeros.append({"Nombre": nombre, "Apellido": apellido})
        else:
            mensaje_confirmacion = QMessageBox()
            mensaje_confirmacion.setIcon(QMessageBox.Warning)
            mensaje_confirmacion.setText(message)
            mensaje_confirmacion.setWindowTitle("Error Insertar Viajero")
            mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
            respuesta = mensaje_confirmacion.exec_()
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)


    def editar_viajero(self, indice_viajero, nombre, apellido):
        """
        Esta función edita un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """        
        self.logica.viajeros[indice_viajero] = {"Nombre":nombre, "Apellido":apellido}
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def eliminar_viajero(self, indice_viajero):
        """
        Esta función elimina un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros.pop(indice_viajero)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)
    
    def mostrar_actividad(self, actividad):
        """
        Esta función muestra la ventana detallada de una actividad
        """
        print ("2 call id_actividad",actividad)
        self.actividad_Amostrar = actividad
        gastos = self.logica.darGastosPorViajeroEnActividad(actividad["id"])

        self.vista_actividad = Vista_actividad(self)
        print("3 call id_actividad", actividad)
        self.vista_actividad.mostrar_gastos_por_actividad(actividad,gastos)

    def insertar_gasto(self, concepto, fecha, valor, id_viajero):
        """
        Esta función inserta un gasto a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        crearGasto = self.logica.adicionarGastoEnActividad(self.actividad_Amostrar["id"], id_viajero, concepto, fecha, valor)
        if not (crearGasto):
            mensaje_confirmacion = QMessageBox()
            mensaje_confirmacion.setIcon(QMessageBox.Warning)
            mensaje_confirmacion.setText("el concepto debe ser de maximo 15 caracteres y el valor < 9999999999")
            mensaje_confirmacion.setWindowTitle("Error")
            mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
            respuesta = mensaje_confirmacion.exec_()
        gastos = self.logica.darGastosPorViajeroEnActividad(self.actividad_Amostrar["id"])
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividad_Amostrar, gastos)

    def editar_gasto(self, gasto_id, concepto, fecha, valor, id_viajero):
        """
        Esta función edita un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """

        editarGasto = self.logica.editarGasto(gasto_id,concepto,fecha,valor,id_viajero)
        if not (editarGasto):
            mensaje_confirmacion = QMessageBox()
            mensaje_confirmacion.setIcon(QMessageBox.Warning)
            mensaje_confirmacion.setText("el concepto debe ser de maximo 15 caracteres y el valor < 9999999999")
            mensaje_confirmacion.setWindowTitle("Error")
            mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
            respuesta = mensaje_confirmacion.exec_()
        gastos = self.logica.darGastosPorViajeroEnActividad(self.actividad_Amostrar["id"])
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividad_Amostrar, gastos)

    def eliminar_gasto(self, indice):
        """
        Esta función elimina un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos.pop(indice)
        self.vista_actividad.mostrar_gastos_por_actividad(self.logica.actividades[self.actividad_actual], self.logica.gastos)

    def mostrar_reporte_compensacion(self,actividad_seleccionada):
        """
        Esta función muestra la ventana del reporte de compensación
        """
        matriz = self.logica.generarReporteCompensacion(actividad_seleccionada["id"])

        self.vista_reporte_comensacion = Vista_reporte_compensacion(self)
        self.vista_reporte_comensacion.mostrar_reporte_compensacion(matriz,actividad_seleccionada)

    def mostrar_reporte_gastos_viajero(self,actividad):
        """
        Esta función muestra el reporte de gastos consolidados
        """
        self.vista_reporte_gastos = Vista_reporte_gastos_viajero(self)
        self.vista_reporte_gastos.mostar_reporte_gastos(self.logica.generarReporteGastos(actividad["id"]),actividad)

    def actualizar_viajeros(self, n_viajeros_en_actividad):
        """
        Esta función añade un viajero a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """

        correcto, mensaje = self.logica.incluirViajeroEnActividad(n_viajeros_en_actividad,self.id_actividad_seleccionada)
        if not (correcto):
            mensaje_confirmacion = QMessageBox()
            mensaje_confirmacion.setIcon(QMessageBox.Warning)
            mensaje_confirmacion.setText(mensaje)
            mensaje_confirmacion.setWindowTitle("Error Insertar Viajero")
            mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
            respuesta = mensaje_confirmacion.exec_()

    def dar_viajeros(self):
        """
        Esta función pasa la lista de viajeros (debe implementarse como una lista de diccionarios o str)
        """
        return self.logica.darViajerosPorActividad(self.actividad_Amostrar["id"])

    def dar_viajeros_en_actividad(self,actividad):
        """
        Esta función pasa los viajeros de una actividad (debe implementarse como una lista de diccionarios o str)
        """
        viajeros = self.logica.darViajerosPorActividad(actividad)
        if viajeros == None:
            return []
        self.id_actividad_seleccionada = actividad
        return viajeros

    def terminar_actividad(self, indice):
        """
        Esta función permite terminar una actividad (debe implementarse)
        """
        pass