# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:02:47 2020

@author: Santiagos
"""
import sys;

from Vista import VentanaInterfaz;
from Modelo import Procesador;
from PyQt5.QtWidgets import QApplication;

#%%
class Controlador(object):                                                                  # Se crea la clase contenedora de
    def __init__(self,vista,procesador):                                                    # la ventana que enlazara la
        self.__mi_vista = vista;                                                            # interfaz y el modelo del sistema
        self.__mi_modelo = procesador;
    
                                                                                            # Peticiones de la interfaz: Interfaz -> Controlador -> Modelo  
    
    def almacenarArchivo(self,archivoCargado,nombre,tamanoEncabezado,canales):                                              
        self.__mi_modelo.almacenarArchivo(archivoCargado,nombre,tamanoEncabezado,canales);                                  
        
    def mostrarCanal(self,canal):                                               
        self.__mi_modelo.mostrarCanal(canal);
                    
    def mostrarCanales(self):
        self.__mi_modelo.mostrarCanales();
    
    def establecerRango(self,x_min,x_max,banderaRango):
        self.__mi_modelo.establecerRango(x_min,x_max,banderaRango);
    
    def limpiarMemoria(self):
        self.__mi_modelo.limpiarMemoria();
        
    def descomponerSenal(self,nivel,umbral,ponderar,dureza):
        self.__mi_modelo.descomponerSenal(nivel,umbral,ponderar,dureza);
        
    def guardarSenal(self,nombreGuardar):
        self.__mi_modelo.guardarSenal(nombreGuardar);
        
                                                                                            # Respuestas del Modelo: Modelo -> Controlador -> Interfaz
    
    def graficarSenal(self,senal):
        self.__mi_vista.graficarSenal(senal);
        
    def graficarSenales(self,senalOriginal,senalFiltrada,senalDescompuesta,detallesFiltrados,umbral,umbrales,nivel_max):
        self.__mi_vista.graficarSenalFiltrada(senalOriginal,senalFiltrada,senalDescompuesta,detallesFiltrados,umbral,umbrales,nivel_max);   

        

#%%    
class Aplicacion(object):                                                                   # Se crea la clase que pone en marcha
    def __init__(self):                                                                     # la aplicacion
        self.__app = QApplication(sys.argv);                                                
        
        self.__mi_vista = VentanaInterfaz();                                                # Se crean los objetos de la aplicacion  
        self.__mi_modelo = Procesador();
        
        self.__mi_controlador = Controlador(self.__mi_vista,self.__mi_modelo);              # Al controlador se le asignan los objetos 
                                                                                            # vista y modelo, y de forma análoga, a los 
        self.__mi_vista.asignarControlador(self.__mi_controlador);                          # objetos se les asigna el controlador  
        self.__mi_modelo.asignarControlador(self.__mi_controlador);                         # para que esten entrelazados
        
    def main(self):
        self.__mi_vista.show();
        sys.exit(self.__app.exec_());
   
     
#%%
aplicacion = Aplicacion();
aplicacion.main();







