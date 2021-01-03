#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 08:33:50 2018

@author: jfochoa
"""
#soporta la carga de multiples tipos de archivos
#si se desea cargar archivos de texto se podria usar numpy.loadtxt
import scipy.io as sio;
# libreria para hacer graficos tipos matlab (pyplot)
import matplotlib.pyplot as plt;
#libreria de manejo de arreglos de grandes dimensiones (a diferencia de las listas basicas de python)
import numpy as np;
#libreria con rutinas de PDS
import scipy.signal as signal;

#PRIMERA PARTE CARGA Y MANIPULACION BASICA

#loading data
#mat_contents = sio.loadmat('D:\Bioseñales 2018-2\Lab2\signals.mat');
mat_contents = sio.loadmat('signals.mat');

#los datos se cargan como un diccionario, se puede evaluar los campos que contiene
print("Los campos cargados son: " + str(mat_contents.keys()));
#la senal esta en el campo data
#data1 = mat_contents['ECG_asRecording'];
data = np.squeeze(mat_contents['ECG_asRecording']);
print("Variable python: " + str(type(data)));
print("Tipo de variable cargada: " + str(data.dtype));
print("Dimensiones de los datos cargados: " + str(data.shape));
print("Numero de dimensiones: " + str(data.ndim));
print("Tamanio: " + str(data.size));
print("Tamanio en memoria (bytes): " + str(data.nbytes));
