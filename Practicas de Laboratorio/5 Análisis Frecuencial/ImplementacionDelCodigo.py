#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:07:22 2020

@author: santiagocardona

PRÁCTICA No 4

Introducción al análisis frecuencial de señales
"""
import matplotlib.pyplot as plt
import numpy as np

#%% 3.2 Representación de señales
'''
supongamos una señal analógica Xa(t) = Asin(2πF0t) con F0= 40Hz y 5V amplitud
será muestrada con Fs = 1000Hz (T = 0.001s). 

'''

Fo = 40 # Frecuencia fundamental de la señal
Tp = 1/Fo # Periodo de la señal
Fs = 1000 # Frecuencia de muestreo
T = 1/Fs # Periodo de muestreo
t = np.arange(0, Tp+T, T) # Por qué Tp + T? Es porque el arange no toma el ultimo valor
# t es una variable Tiempo para un ciclo de la señal con duración 
# de Tp más una muestra T
A = 5
x = A*np.sin(2*np.pi*Fo*t)
plt.plot(t, x, marker='o')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid();

'''
Existe un procedimiento alternativo para la creación de la señal con las 
condiciones de muestreo, amplitud y demás especificaciones de la anterior

'''

fo = Fo/Fs # Frecuencia normalizada
n = np.arange(0, len(t))
x1 = A*np.sin(2*np.pi*fo*n) 
plt.plot(n, x1, marker='o')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid();

# a) Compruebe que los valores de las primeras cinco muestras son los mismos.
print("\nSeñal analógica (primeros 5 datos)")
print(x[n<5])
print("\nSeñal discreta (primeros 5 datos)")
print(x1[n<5])

plt.plot(x[n<5], marker='D')
plt.plot(x1[n<5], marker=',')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.legend(['análogica','muestreada']);
plt.grid();

#%%
'''
Adicional al procedimiento alternativo para la generación de la señal, tambien 
existe una manera diferente para la graficación. Aunque no va a ser la utilizada
se utiliza la función stem en el siguiente gráfico

'''
plt.stem(n, x1) #, marker='o'
plt.xlabel('Muestras')
plt.ylabel('Amplitud')

#%%  3.3 Energía y potencia en el dominio del tiempo

# La energía en un ciclo de la señal x(n) se puede hallar de la siguiente manera:

energia = sum(x**2)

#La potencia media de la señal medida en W es:

potencia = energia/(len(t)-1)

# El valor cuadrático medio es la raíz cuadrada de la potencia:

rms = np.sqrt(potencia)

# Ahora la energía y potencia considerando 10 ciclos de la sinusoide (250ms)

t10 = np.arange(0, 10*Tp+T, T)
x10 = A*np.sin(2*np.pi*Fo*t10)
energia10 = sum(x10**2)
potencia10 = energia10/(len(t10)-1)
rms10 = np.sqrt(potencia)

print("\nPara 1 Ciclo (25ms):")
print("Energía: % s" %round(energia,2))
print("Potencia: % s" %round(potencia,2))
print("rms: % s" %round(rms,2))

print("\nPara 10 Ciclos (250ms):")
print("Energía: % s" %round(energia10,2))
print("Potencia: % s" %round(potencia10,2))
print("rms: % s" %round(rms10,2))

""" responder b) La potencia es la misma que en x(n). ¿Por qué? """
# Porque la potencia está asociada con la frecuencia, y al ser ciclos
# de la misma señal, la frecuencia es la misma, y por tanto igual lo
# será su potencia.

#%% 3.4 Análisis de Fourier en tiempo discreto

# cálculo de la DFT de la señal

X10 = np.fft.fft(x10)

# Representación gráfica de la FFT. 

plt.plot(abs(X10))
plt.title('Módulos de la DFT')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')

# para extraer información y conclusiones de la señal original xa(t), deberemos
# trabajar con F = (k * Fs)/N

N = len(X10)
F = np.arange(0,N)*Fs/N
plt.plot(F,abs(X10))
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')

# debido a la simetría que poseen todas las DFT suele usarse la mitad de la 
# gráfica para su análisis, Este valor “mitad” de la frecuencia de muestreo
# también recibe el nombre de frecuencia Nyquist.

Nmitad = int(np.ceil(N/2))
Fmitad = np.arange(0,Nmitad)*Fs/N
X10mitad = X10[0:Nmitad]
plt.plot(Fmitad,abs(X10mitad))
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')

# Realizando un zoom se observa que la componente frecuencial se encuentra 
# ubicada a 40 Hz.

plt.plot(Fmitad,abs(X10mitad))
plt.ylabel('Amplitud')
plt.xlabel('Frecuencia (Hz)')
plt.xlim(0,80)

#%%

F1 = np.fft.fft(x);
F2 = np.zeros((len(F1)));
F2[9:13] = F1[9:13];
xr = np.fft.ifft(F2);
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t, np.real(xr))
ax.set(xlabel='Tiempo (s)', ylabel='Amplitud (V)');
plt.show()

#%%
plt.show()













