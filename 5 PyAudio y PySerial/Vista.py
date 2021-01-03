# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 18:59:09 2020

@author: USER
"""

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout  # Librerias necesarias para crear ventanas
from PyQt5.uic import loadUi
from pyqtgraph.Qt import QtCore

import numpy as np
import pyaudio # Libreria PyAudio
import struct

import serial # Libreria PySerial

from matplotlib.figure import Figure;
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#%%
class FiguraCanvas(FigureCanvas):                                                           # Clase Figura creada para graficar 
    def __init__(self, parent= None, ancho = 741, alto = 600, dpi = 100):                   # la densidad espectral de potencia de
        self.fig = Figure(figsize = (ancho, alto), dpi = dpi)                               # 3 dimensiones (t,f,PSD)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)

    def graficar(self,data):
        
        self.axes.clear();
        self.axes.set_ylim(-12000,12000)
        line, = self.axes.plot(data)
        line.set_ydata(data)
         
        self.axes.figure.canvas.draw()
        self.axes.figure.canvas.flush_events()
        

#%%
class VentanaInterfaz(QMainWindow):
    def __init__(self,ppal = None):
        super(VentanaInterfaz,self).__init__();                                            
        loadUi('Interfaz.ui',self) 
        self.campoGrafico.hide()
        self.estructura();  
        
    def asignarControlador(self,controlador):                                               
        self.__controlador = controlador 
        
    def estructura(self):
        layout = QVBoxLayout();
        self.campoGrafico.setLayout(layout)  # Campo para graficar el audio                                             
        self.figura = FiguraCanvas(self.campoGrafico, ancho = 741, alto = 401, dpi = 100)
        layout.addWidget(self.figura)
        
        self.Psoc = serial.Serial("COM3", 9600) # Objeto de la clase PySerial
        
    def audio(self):
        CHUNK = 1024  # Muestras mostradas por segundo
        FORMAT = pyaudio.paInt16    # formato de bits (entero sin signo)
        CHANNELS = 1    # 1 solo microfono como canal
        RATE = 44100    # frecuencia de muestreo (mas comun 44100)
        
        p = pyaudio.PyAudio()   # Se crea un objeto de la clase PyAudio
        
        stream = p.open(    # object stream o de emision
                format=FORMAT,          # recibe el formato, cantidad de canales,
                channels=CHANNELS,      # frecuencia de muestreo, 
                rate=RATE,              # entrada = salida = True por defecto
                input=True,             # muestras presentadas en cada segundo (frames)
                output=True,
                frames_per_buffer=CHUNK
                )
        
        data = stream.read(CHUNK)       # Se lee la muestra
        data16 = np.frombuffer(data,dtype = np.int16)   # se transforma en un arreglo de bits
        data_int = np.array(struct.unpack(str(CHUNK) + 'h',data16))
        
        self.figura.graficar(data_int)
    
    def start(self):
        self.campoGrafico.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.audio)
        self.timer.start(5)
    
    def stop(self):
        self.campoGrafico.hide()
        self.timer.stop()
        self.Psoc.close()
        
        
#%%
    def recibirDato(self):
        numero = ord(self.Psoc.read())
        self.numeroRecibido.setValue(numero)
        print(numero)
        
    def enviarDato(self):
        numero = str(self.numeroEnviado.value())    # el número leido se convierte a str
        self.Psoc.write(numero.encode('utf-8'))     # para poder codificarlo a binario
                                                    # y se envia al Psoc
                                                    
        
        
        
        