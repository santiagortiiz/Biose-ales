# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:02:52 2020

@author: Santiagos
"""

from PyQt5.QtWidgets import QMainWindow, QFileDialog;                                       # Librerias necesarias para crear ventanas
from PyQt5.uic import loadUi;

import numpy as np;


#%%
class VentanaInterfaz(QMainWindow):
    def __init__(self,ppal = None):
        super(VentanaInterfaz,self).__init__();                                             # Carga la venta de QtDesigner
        loadUi('VentanaInterfaz.ui',self);  
        self.bandera = 0;
        self.estructura();                                                                  # Llama la estructura de la ventana
        
    def asignarControlador(self,controlador):                                               # Se asigna el controlador a la ventana de inicio
        self.__controlador = controlador;   
        
    def estructura(self):                                                                   # Se conectan los botones de la ventana con sus
                                                                                            # respectivas funciones
        self.botonCargar.clicked.connect(self.cargarArchivo);
        self.botonCanal.clicked.connect(self.mostrarCanal);
        self.botonCanales.clicked.connect(self.mostrarCanales);
        self.botonRango.clicked.connect(self.banderaRango0);                         
        self.botonRestablecer.clicked.connect(self.banderaRango1);
        self.botonLimpiar.clicked.connect(self.limpiarMemoria);
        
        self.ocultar();
        
        self.botonFiltrar.activated[str].connect(self.filtrarSenal);                        # En esta zona estan los elementos que ejecutan
        self.botonUmbral.activated[str].connect(self.filtrarSenal);                         # las acciones de filtrado
        self.botonPonderar.activated[str].connect(self.filtrarSenal);
        self.botonDureza.activated[str].connect(self.filtrarSenal);
        self.botonGuardar.clicked.connect(self.guardarSenal);
        
        self.botonCanal.setEnabled(False);                                                  # Se desactivan los elementos que no pueden usarse
        self.botonCanales.setEnabled(False);                                                # hasta cumplir x condición
        
        self.botonGuardar.setEnabled(False);
        self.botonFiltrar.setEnabled(False);
        self.botonUmbral.setEnabled(False);
        self.botonPonderar.setEnabled(False);
        self.botonDureza.setEnabled(False);
        
#%%   
    def cargarArchivo(self):
        archivoCargado, _ = QFileDialog.getOpenFileName(self,"Abrir Señal","",
                                                             "Todos los archivos (*);; Archivos mat(*.mat)");
        
        self.bandera = 0;                
        self.tiempoMax.setMaximum(500000);
        self.botonCanal.setEnabled(False);                                                  # Se desactivan los elementos que no pueden usarse
        self.botonCanales.setEnabled(False);                                                # hasta cumplir x condición
        
        self.botonGuardar.setEnabled(False);
        self.botonFiltrar.setEnabled(False);
        self.botonUmbral.setEnabled(False);
        self.botonPonderar.setEnabled(False);
        self.botonDureza.setEnabled(False);
        
        if archivoCargado.endswith(".mat"):                                                 # Analiza si la ruta del archivo cargada es 
            nombre = str(self.campoNombre.text());                                          # .mat o .txt y si cumple la condición, envia
                                                                                            # las variables necesarias al modelo para
            if nombre != ('' or 'Nombre señal .mat'):                                       # mostrar las señales contenidas
                self.campoNombre.setText('Nombre señal .mat');
                tamanoEncabezado = 0;
                canales = 0;
                self.aparecer();
                self.__controlador.almacenarArchivo(archivoCargado,nombre,tamanoEncabezado,canales);
            
        elif archivoCargado.endswith(".txt"):
            tamanoEncabezado = int(self.campoEncabezado.text());
            canales = int(self.campoCanales.text());
            if tamanoEncabezado != ("Tamaño encabezado .txt" or '') and canales != ("Cantidad canales .txt" or ''):
                self.campoEncabezado.setText("Tamaño encabezado .txt");
                self.campoCanales.setText("Cantidad canales .txt");
                nombre = None;
                self.aparecer();
                self.__controlador.almacenarArchivo(archivoCargado,nombre,tamanoEncabezado,canales);
                             
          
#%%                                                   
    def graficarSenal(self,senal):                                                          # Recibe una señal mono/multi canal,
        self.campoOriginal.clear();                                                         # la grafica y limita el QSpinBox
                                                                                            # al numero de canales de la señal.
        if senal.ndim == 1:                                                                 # Además se habilitan los demás botones de la interfaz
            self.campoOriginal.plot(senal,pen=('b'))                                        
            
            if self.bandera == 0:                                                           # self.bandera evita que siempre que siempre se 
                #self.tiempoMin.setMaximum(len(senal));                                      # sobrecarguen los trabajos, habilitando los botones
                #self.tiempoMax.setMaximum(len(senal));                                      # solo 1 vez
                self.tiempoMax.setValue(len(senal));
                self.botonFiltrar.setEnabled(True);
                self.botonUmbral.setEnabled(True);
                self.botonPonderar.setEnabled(True);
                self.botonDureza.setEnabled(True);
                
        else:
            canales = senal.shape[0];
            
            DC = 20;
            
            for canal in range(canales):
                self.campoOriginal.plot(senal[canal,:] + DC*canal,pen=('b'));
            self.campoOriginal.repaint();
            
            if self.bandera == 0:
                #self.tiempoMin.setMaximum(senal.shape[1]);
                #self.tiempoMax.setMaximum(senal.shape[1]);
                self.tiempoMax.setValue(senal.shape[1]);
                
                self.seleccionarCanal.setMinimum(1);
                self.seleccionarCanal.setMaximum(canales);
                
                self.botonCanal.setEnabled(True);                                           
                self.botonCanales.setEnabled(True);
                self.botonFiltrar.setEnabled(True);
                
        self.bandera = 1;
        
        
    def mostrarCanal(self):
        self.botonFiltrar.setEnabled(True);                                                 # Se habilitan los elementos que permiten 
        self.botonUmbral.setEnabled(True);                                                  # filtrar la señal de un canal
        self.botonPonderar.setEnabled(True);
        self.botonDureza.setEnabled(True);
        canal = self.seleccionarCanal.value();                                              # Se lee el canal que desea visualizarse
        self.__controlador.mostrarCanal(canal-1);                                           # y se le pide al modelo mediante el controlador         
        
    def mostrarCanales(self):
        self.botonGuardar.setEnabled(False);                                                # Se deshabilitan los elementos de filtrado
        self.botonFiltrar.setEnabled(False);
        self.botonUmbral.setEnabled(False);
        self.botonPonderar.setEnabled(False);
        self.botonDureza.setEnabled(False);
        self.__controlador.mostrarCanales();
        
    def banderaRango0(self):                                                                # Las funciones banderaRangoN determinan si se
        self.establecerRango(0);                                                            # desea ver un rango o toda la señal
                                                                                            # rango0 : establecer
                                                                                            # rango1 : restablecer
    def banderaRango1(self):
        self.bandera = 0;                                                                   # Escribe el limite maximo de muestras cuando se restablece
        self.establecerRango(1);                                                            
        
    def establecerRango(self,banderaRango):                                                 # Se lee el boton de los spinBox x_min y x_max,                                         
        x_min = self.tiempoMin.value();                                                     # y se pide al controlador analizar rangos y bandera                                          
        x_max = self.tiempoMax.value();                                                     # para graficar la señal deseada
        
        if x_min < x_max:
            self.__controlador.establecerRango(x_min,x_max,banderaRango);
        
    def limpiarMemoria(self):                                                               # Limpia la memoria del sistema borrando los 
        self.bandera = 0;                                                                   # registros que quedaron como atributos
        self.campoOriginal.clear();                                                         # en la instancia de la clase Procesador
        self.campoFiltro.clear();
        
        self.botonCanal.setEnabled(False);
        self.botonCanales.setEnabled(False);
        self.botonFiltrar.setEnabled(False);
        self.botonGuardar.setEnabled(False);
        self.botonFiltrar.setEnabled(False);
        self.botonUmbral.setEnabled(False);
        self.botonPonderar.setEnabled(False);
        self.botonDureza.setEnabled(False);
        self.ocultar();
        
        self.__controlador.limpiarMemoria(); 
    
    def aparecer(self):
        self.campoOriginal.show();
        self.campoFiltro.show();
        self.tiempoMin.show();
        self.tiempoMax.show();
        self.botonRango.show();
        self.botonRestablecer.show();
        self.botonCanal.show();
        self.botonCanales.show();
        self.botonFiltrar.show();
        self.botonUmbral.show();
        self.botonPonderar.show();
        self.botonDureza.show();
        self.nivelDescmpn.show();
        self.nivel.show();
        self.botonGuardar.show();
        self.nombreGuardar.show();
        self.seleccionarCanal.show();
        
    def ocultar(self):
        self.campoOriginal.hide();
        self.campoFiltro.hide();
        self.tiempoMin.hide();
        self.tiempoMax.hide();
        self.botonRango.hide();
        self.botonRestablecer.hide();
        self.botonCanal.hide();
        self.botonCanales.hide();
        self.botonFiltrar.hide();
        self.botonUmbral.hide();
        self.botonPonderar.hide();
        self.botonDureza.hide();
        self.nivelDescmpn.hide();
        self.nivel.hide();
        self.botonGuardar.hide();
        self.nombreGuardar.hide();
        self.seleccionarCanal.hide();
        
    def guardarSenal(self):
        nombreGuardar = str(self.nombreGuardar.text());
        self.nombreGuardar.setText('Nombre señal');
        self.__controlador.guardarSenal(nombreGuardar);

#%%    
    def filtrarSenal(self):                                                                 # Lee los parámetros de filtro y los envía 
        self.botonGuardar.setEnabled(True);                                                 # al modelo para ejecutar el proceso de 
        umbral = self.botonUmbral.currentText();                                            # filtrado del canal respectivo
        ponderar = self.botonPonderar.currentText();
        dureza = self.botonDureza.currentText();
        nivel = self.nivel.value();
        
        if (umbral == 'Umbral') or (umbral == 'Sure'):                                      # En caso de no haber seleccionado ningun
            umbral = 'Universal';                                                           # parámetros éstos se establecen por defecto
        if ponderar == 'Ponderar':
            ponderar = 'Común';
        if dureza == 'Dureza':
            dureza = 'Duro';
    
        self.__controlador.descomponerSenal(nivel,umbral,ponderar,dureza);    
            
#%%        
    def graficarSenalFiltrada(self,senalOriginal,senalFiltrada,senalDescompuesta,detallesFiltrados,umbral,umbrales,nivel_max):
        ponderar = self.botonPonderar.currentText();
        ver = self.botonFiltrar.currentText();
        self.nivel.setMaximum(nivel_max);
        
        if ver == 'Aplicar filtro':                                                         # Esta función recibe del modelo  
            ver = 'Ver filtrada';                                                           # varios aspectos resultantes de las etapas 
                                                                                            # de descomposición, filtrado y reconstrucción 
        if ver == 'Ver filtrada':                                                           # para que el usuario tenga la posibilidad de 
            self.campoFiltro.clear();                                                       # graficar, comparar y analizar
            self.campoFiltro.plot(senalFiltrada,pen=('r'));
            self.campoFiltro.repaint();
            
        elif ver == 'Ver original':
            self.campoFiltro.clear();
            self.campoFiltro.plot(senalOriginal,pen=('b'));
            self.campoFiltro.repaint();
            
        elif ver == 'Comparar':
            self.campoFiltro.clear();
            self.campoFiltro.plot(senalOriginal,pen=('b'));
            self.campoFiltro.plot(senalFiltrada,pen=('r'));
            self.campoFiltro.repaint();
        
        elif ver == 'Aprox y detalles':                                                     # Sí el usuario desea ver la señal descompuesta
            self.campoFiltro.clear();                                                       # analiza la opción de ponderación escogida
                                                                                            # para determinar si deben mostrarse uno
            self.campoFiltro.plot(senalDescompuesta,pen=('b'));                             # o varios umbrales (uno por cada detalle
                                                                                            # en la opción Multi nivel)
            if ponderar == 'Multi nivel':
                for i in (umbrales):
                    self.campoFiltro.plot(i*np.ones(len(senalDescompuesta)),pen=('y'));
                    self.campoFiltro.plot(-i*np.ones(len(senalDescompuesta)),pen=('y'));
            
            else:
                self.campoFiltro.plot(umbral*np.ones(len(senalDescompuesta)),pen=('y'));
                self.campoFiltro.plot(-umbral*np.ones(len(senalDescompuesta)),pen=('y'));
            
            self.campoFiltro.repaint();
            
        elif ver == 'Detalles filtrados':
            self.campoFiltro.clear();
            
            for detalleFiltrado in detallesFiltrados:
                self.campoFiltro.plot(detalleFiltrado,pen=('r'));
            
            if ponderar == 'Multi nivel':
                for i in range(len(umbrales)):
                    self.campoFiltro.plot(i*np.ones(len(senalDescompuesta)),pen=('y'));
                    self.campoFiltro.plot(-i*np.ones(len(senalDescompuesta)),pen=('y'));
            
            else:
                self.campoFiltro.plot(umbral*np.ones(len(senalDescompuesta)),pen=('y'));
                self.campoFiltro.plot(-umbral*np.ones(len(senalDescompuesta)),pen=('y'));
            
            self.campoFiltro.repaint();
        
                             
                                                             
                                                             
                                                             
                                                             
                                                             
                                                             
                                                             
                                                             
                                                             
       