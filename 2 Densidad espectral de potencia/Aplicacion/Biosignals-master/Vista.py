# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:02:52 2020

@author: Santiagos
"""

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout;                          # Librerias necesarias para crear ventanas
from PyQt5.uic import loadUi;

import numpy as np;

from matplotlib.figure import Figure;
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#%%
class FiguraCanvas(FigureCanvas):                                                           # Clase Figura creada para graficar 
    def __init__(self, parent= None, ancho = 700, alto = 600, dpi = 100):                   # la densidad espectral de potencia de
        self.fig = Figure(figsize = (ancho, alto), dpi = dpi);                              # 3 dimensiones (t,f,PSD)
        self.axes = self.fig.add_subplot(111);
        
        FigureCanvas.__init__(self,self.fig);

    def graficar_espectro(self,time, f, PSD, bwMin, bwMax):
        
        self.axes.clear()
        self.axes.contourf(time,
                           f[(f >= bwMin) & (f <= bwMax)],
                           PSD[(f >= bwMin) & (f <= bwMax),:],
                           100, # Especificar 20 divisiones en las escalas de color 
                           extend='both')
        
        self.axes.set_xlabel('Duración de la señal [segundos]');
        self.axes.set_ylabel('Fr    ecuencia [Hz]');
                    
        self.axes.figure.canvas.draw()
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
        
        
        self.botonPSD.activated[str].connect(self.calcularPSD);
        
        
        
        self.botonCanal.setEnabled(False);                                                  # Se desactivan los elementos que no pueden usarse
        self.botonCanales.setEnabled(False);                                                # hasta cumplir x condición
        
        self.botonGuardar.setEnabled(False);
        self.botonFiltrar.setEnabled(False);
        self.botonUmbral.setEnabled(False);
        self.botonPonderar.setEnabled(False);
        self.botonDureza.setEnabled(False);
        
        layout = QVBoxLayout();
        self.campoGrafico.setLayout(layout);                                                # Inserto un QVBox en el campoGrafico
        self.figura = FiguraCanvas(self.campoGrafico, ancho = 7, alto = 5, dpi = 100);
        layout.addWidget(self.figura);
        
        
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
                #self.tiempoMin.setMaximum(len(senal));                                     # sobrecarguen los trabajos, habilitando los botones
                #self.tiempoMax.setMaximum(len(senal));                                     # solo 1 vez
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
        
        if self.botonPSD.currentText() == "PSD Welch":
            self.tamanoVentana.setValue(x_max);
            self.solapamiento.setValue(x_max/2);
        
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
        self.botonLimpiar.show();
        
        self.botonPSD.show();
        self.labelFs.show();
        self.fs.show();
        self.botonBW.show();
        self.bwMin.show();
        self.bwMax.show();
        
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
        self.botonLimpiar.hide();
        
        self.botonPSD.hide();
        self.labelFs.hide();
        self.fs.hide();
        self.botonBW.hide();
        self.bwMin.hide();
        self.bwMax.hide();
        
        self.ocultarWelch();
        self.ocultarMultitaper();
        
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
        self.campoGrafico.hide();
        
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
        
        if ver == 'Filtro Wavelet':                                                         # Esta función recibe del modelo  
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

#%%        
    def establecerBwMin(self):                                                              # En el método Welch se establece por
        tamanoVentana = self.tamanoVentana.value();                                         # defecto, un solapamiento del 50%
        solapamiento = tamanoVentana/2;          
        self.solapamiento.setValue(solapamiento);

#%%       
    def calcularPSD(self):                                                                  # Esta funcion pide al modelo el 
        metodo = self.botonPSD.currentText();                                               # calculo del PSD de acuerdo al
        fs = self.fs.value();                                                               # método seleccionado por el usuario
        self.bwMin.setMaximum(fs);
        self.bwMax.setMaximum(fs);
        
        if (metodo == '|Armónicos|') or (metodo == 'PSD crudo'):
            self.ocultarWelch();                                                            # Si desea ver los armónicos de la
            self.ocultarMultitaper();                                                       # señal o el PSD directo, se ocultan
            self.botonTipoVentana.hide();                                                   # los parámetros de los otros métodos
            self.botonEscala.hide();
            self.__controlador.calcularPSD(metodo,fs);
        
        elif metodo == 'PSD Welch':                                                         # Se ocultan los parametros del método
            self.ocultarMultitaper();                                                       # multitaper, y solo se muestran los
            self.mostrarWelch();                                                            # del Welch
            tipoVentana = self.botonTipoVentana.currentText();
            tamanoVentana = self.tamanoVentana.value();
            solapamiento = self.solapamiento.value();
            escala = self.botonEscala.currentText();
            
            if tamanoVentana > 3:                                                           # El solapamiento máximo puede
                self.solapamiento.setMaximum(tamanoVentana);                                # ser el tamaño de la ventana
            
            if tipoVentana == 'Tipo Ventana':                                               # En estos 3 condicionales, se establecen
                tipoVentana = 'bartlett';                                                   # Valores por defecto de tipo de ventana
                                                                                            # y escala, en caso de que el usuario
            if (escala == 'Escala') or (escala == 'Espectro [V^2]'):                                       # no los indique
                escala = 'spectrum';
                
            elif escala == 'Densidad [V^2/Hz]':
                escala = 'density';
            
            if tamanoVentana > solapamiento:
                self.__controlador.calcularPSD_Welch(fs,tipoVentana,
                                                     tamanoVentana,solapamiento,escala);
                
        elif metodo == 'PSD Multi-taper':
            self.ocultarWelch();                                                            # Se ocultan los parametros del Welch
            self.mostrarMultitaper();                                                       # y se muestran solo los de Multitaper
            segmentos = self.segmentos.value();
            fcMin = self.fcMin.value();
            fcMax = self.fcMax.value();
            W = self.W.value();
            T = self.T.value();
            p = self.p.value();
            trialAverage = self.trialAverage.value();
            
            if fcMin < fcMax:                                                               # Se verifique que la banda pasante
                self.__controlador.calcularPSD_Multitaper(segmentos,fs,fcMin,fcMax,         # escogida sea correcta
                                                          W,T,p,trialAverage);
                
        elif metodo == 'Tiempo frecuencia':
            self.ocultarWelch();                                                            # Si el metodo es Tiempo frecuencia
            self.ocultarMultitaper();
            self.mostrarTiempoFrecuencia();
            fcMin = self.fcMin.value();                                                     # solo se muestran parametros para
            fcMax = self.fcMax.value();                                                     # determinar la banda de interés
            bwMin = self.bwMin.value();
            bwMax = self.bwMax.value();
            
            if (fcMax - fcMin) < 2:
                self.fcMax.setValue(50);
                fcMax = self.fcMax.value(); 
                self.fcMin.setValue(10);
                fcMin = self.fcMin.value();
                
            if (fcMin < fcMax and fcMin < bwMax):
                self.__controlador.calcularWaveletContinuo(fs,fcMin,fcMax);
            
    
    def graficarPSD(self,f,datos):
        bwMin = self.bwMin.value();                                                         # Lee los rangos de frecuencias
        bwMax = self.bwMax.value();                                                         # y el estado actual del metodo
        metodo = self.botonPSD.currentText();                                               # para determinar lo que debe graficar
        
        if metodo == 'PSD Multi-taper':
            trialAverage = self.trialAverage.value();
        else:
            trialAverage = 1;
            
        
        if bwMin < bwMax:
            if (trialAverage == 1):                                                         # Analiza trial average y si el 
                self.campoFiltro.clear();                                                   # metodo seleccionado es multitaper
                self.campoFiltro.plot(f[(f >= bwMin) & (f <= bwMax)],                       # o no, para graficar uno ó multiples PSD            
                                        datos[(f >= bwMin) & (f <= bwMax)],
                                        pen=('r'));
                self.campoFiltro.repaint();
            else:
                self.campoFiltro.clear(); 
                
                for i in range(datos.shape[1]):                                                      
                    self.campoFiltro.plot(f[(f >= bwMin) & (f <= bwMax)],
                                            datos[:,i][(f >= bwMin) & (f <= bwMax)],
                                            pen=('r'));
                    self.campoFiltro.repaint();
                
                
    def graficarWaveletContinuo(self,tiempo,f,PSD):
        bwMin = self.bwMin.value();
        bwMax = self.bwMax.value();
        print(PSD.ndim);
        
        if (bwMin < bwMax) and (PSD.ndim >= 2):
            self.figura.graficar_espectro(tiempo,f,PSD,bwMin,bwMax);
        
    def WaveletContinuo(self,tiempo,f,PSD):
        bwMin = self.bwMin.value();                                                         # Actualmente no funciona, no se sabe como
        bwMax = self.bwMax.value();                                                         # imponer 3 ejes en un graphics view
        
        if bwMin < bwMax:
            self.campoFiltro.clear();
            self.campoFiltro.contourf(tiempo,
                                  f[(f>=bwMin) & (f<=bwMax)],
                                  PSD[(f>=bwMin) & (f<=bwMax),:],
                                  pen=('r'));
            print('Pasa pero no dibuja nada');
            self.campoFiltro.repaint();
                

#%%
    def mostrarWelch(self):                                                                 # Estas funciones permiten controlar
        self.botonTipoVentana.show();                                                       # los parámetros con los cuales
        self.botonEscala.show();                                                            # el usuario puede interactuar
        self.labelTamanoVentana.show();
        self.labelSolapamiento.show();
        self.tamanoVentana.show();
        self.solapamiento.show();
        self.campoGrafico.hide();
        
    def ocultarWelch(self):
        self.botonTipoVentana.hide();
        self.botonEscala.hide();
        self.labelTamanoVentana.hide();
        self.labelSolapamiento.hide();
        self.tamanoVentana.hide();
        self.solapamiento.hide();
        
    def mostrarMultitaper(self):
        self.labelSegmentos.show();
        self.labelTrialAv.show();
        self.labelW.show();
        self.labelT.show();
        self.labelP.show();
        self.segmentos.show();
        self.W.show();
        self.T.show();
        self.p.show();
        self.botonBandaPaso.show();
        self.fcMin.show();
        self.fcMax.show();
        self.trialAverage.show();
        self.campoGrafico.hide();
        
    def ocultarMultitaper(self):
        self.labelSegmentos.hide();
        self.labelTrialAv.hide();
        self.labelW.hide();
        self.labelT.hide();
        self.labelP.hide();
        self.segmentos.hide();
        self.W.hide();
        self.T.hide();
        self.p.hide();
        self.botonBandaPaso.hide();
        self.fcMin.hide();
        self.fcMax.hide();
        self.trialAverage.hide();
        self.campoGrafico.hide();
        
    def mostrarTiempoFrecuencia(self):
        self.botonBW.show();
        self.bwMin.show();
        self.bwMax.show();
        self.botonBandaPaso.show();
        self.fcMin.show();
        self.fcMax.show();
        self.campoGrafico.show();