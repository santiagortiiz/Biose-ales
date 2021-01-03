# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 18:59:00 2020

@author: USER
"""

import scipy.io as sio;                                                                     # Librerias necesarias para extraer informacion
from csv import reader as reader_csv;                                                       # de archivos .mat y .txt

import numpy as np;
import math;

import scipy.signal as signal;
from scipy.fftpack import fft;

#%%
class Procesador(object):
    def __init__(self):                                                                     # Se inicializan los atributos que tendra el modelo 
        pass;
        
    def asignarControlador(self,controlador):                                               # Se asigna el controlador al modelo
        self.__controlador = controlador;
        
        
        
        
        
        