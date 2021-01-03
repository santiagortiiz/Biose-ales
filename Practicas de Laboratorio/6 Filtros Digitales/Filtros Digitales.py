# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:06:48 2020

@author: SANTIAGO
"""

from Bode import bode

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

#%% 1) Señal fisiológica real 
fo = 0.01
fs = 25
n = np.arange(0,1001) # Vector de 1000 muestras
#t = np.arange(0, 1000/fs, 1/fs) # Vector de tiempo (inicio, fin - 1, pasos: Periodo de muestreo)
xe = np.sin(2*np.pi*fo*n)

plt.figure()
plt.plot(n,xe)
plt.title('Señal real x_e')
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.grid();

#%% 2) Señal fisiológica registrada (atenuada, desfasada y ruidosa)

#Ruido Gausiano
mu, sigma = 0, 0.1 # media, desviación estándar
ruido = np.random.normal(mu, sigma, len(n))
atenuacion = 0.8
desfase = -15
ye = atenuacion*np.sin(2*np.pi*fo*n + desfase) + ruido

plt.figure()
plt.plot(n,ye)
plt.title('Señal captada y_e')
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.grid();

#%% 3) Comparación
plt.figure()
plt.plot(n,xe)
plt.plot(n,ye)
plt.title('Comparacion de señales')
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.legend(['Señal real','Señal Capturada'])
plt.grid();

#%% 4) Diseño de filtros FIR: signal.firwin(numtaps,cutoff,width,window,pass_zero,scale,fnyq,fs)
fnyq = fs/2

#%%
# Pasa Bajas FIR
orden = 10
fc = 1.25 # Hz
fc_normalizada = fc/fnyq

# Coeficientes
a = 1
b = signal.firwin(orden+1,fc_normalizada,window='hamming',pass_zero='lowpass')
pasa_bajas_fir = [a,b]

# Diagrama de Bode del filtro diseñado
bode(b,a,orden)

#%%
# Pasa Altas FIR
# Cambios: Debe procurarse que si la banda de paso contiene la Fnyq, el orden
# del filtro debe ser impar, además pass_zero debe ser 'highpass'
orden = 30
fc = 7.5 # Hz
fc_normalizada = fc/fnyq

if (orden%2 == 0): orden = orden + 1;
# Coeficientes
a = 1
b = signal.firwin(orden,fc_normalizada,window='hamming',pass_zero='highpass')

# Diagrama de Bode del filtro diseñado
bode(b,a,orden)

#%%
# Pasa Banda FIR
# Cambios: En lugar de una frecuencia de corte, se ingresa una tupla que 
# contenga la frecuencia baja y la alta, además pass_zero debe ser 'bandpass'
orden = 30
f_baja = 1.5 # Hz
f_baja = f_baja/fnyq
f_alta = 7.5
f_alta = f_alta/fnyq

# Coeficientes
a = 1
b = signal.firwin(orden+1,[f_baja,f_alta],window='hamming',pass_zero='bandpass')

# Diagrama de Bode del filtro diseñado
bode(b,a,orden)

#%% 5) Diseño de Filtros IIR
#signal.iirfilter(N, Wn, rp=None, rs=None, btype='band', analog=False, ftype='butter', output='ba', fs=None
fnyq = fs/2

#%%
# Pasa Bajas IIR
orden = 30
fc = 1.25 # Hz
fc_normalizada = fc/fnyq

# Coeficientes
b,a = signal.iirfilter(orden,fc_normalizada,btype='lowpass',output='ba')
pasa_bajas_iir = [a,b]

# Diagrama de Bode del filtro diseñado
bode(b,a,orden)

#%%
# Pasa Altas IIR
# Cambios: Debe procurarse que si la banda de paso contiene la Fnyq, el orden
# del filtro debe ser par, además pass_zero debe ser 'highpass'
orden = 30
fc = 7.5 # Hz
fc_normalizada = fc/fnyq

# Coeficientes
b,a = signal.iirfilter(orden,fc_normalizada,btype='highpass',output='ba')

# Diagrama de Bode del filtro diseñado
bode(b,a,orden)

#%%
# Pasa Banda IIR
# Cambios: En lugar de una frecuencia de corte, se ingresa una tupla que 
# contenga la frecuencia baja y la alta, además pass_zero debe ser 'bandpass'
orden = 30
f_baja = 1.25 # Hz
f_baja = f_baja/fnyq
f_alta = 7.5
f_alta = f_alta/fnyq

# Coeficientes
b,a = signal.iirfilter(orden,[f_baja,f_alta],btype='bandpass',output='ba')

# Diagrama de Bode del filtro diseñado
bode(b,a,orden)

#%% Comparación

# Pasa Bajas: El filtro FIR funcionó bien, sin embargo, el filtro IIR atenúo 
# y distorsiono la banda pasante debido al orden del filtro tan elevado

# Pasa Altas: Ambos filtros presentan el comportamiento deseado, sin embargo
# la pendiente del filtro IIR es mas brusca

# Pasa Banda: Ambos filtros son adecuados, sin embargo el IIR tiene una escala
# de atenuación en la banda de rechazo muchisimo mayor

#%% 6) Filtrado

# Pasa bajas FIR

plt.figure()
plt.subplot(2,1,1)

ye_pasa_bajas_fir = signal.lfilter(pasa_bajas_fir[1],pasa_bajas_fir[0],ye)
plt.plot(n,ye)
plt.plot(n,ye_pasa_bajas_fir)
plt.title('Antes/Despues de filtrar Pasa bajas FIR')
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.legend(['Señal capturada','Señal filtrada (lfilt)'])
plt.grid()

plt.subplot(2,1,2)
ye_pasa_bajas_fir = signal.filtfilt(pasa_bajas_fir[1],pasa_bajas_fir[0],ye)
plt.plot(n,ye)
plt.plot(n,ye_pasa_bajas_fir)
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.legend(['Señal capturada','Señal filtrada (filtfilt)'])
plt.grid()

plt.tight_layout()
# ¿Por qué se utiliza sólo el numerador? ¿A qué hace referencia el numerador? 
# ¿Evidencia cambios en el uso de las funciones de filtrado? ¿Cómo se puede 
#explicar la falta de coincidencia? ¿Es adecuado el orden del filtro usado? 

# En este caso se emplea solo el numerador dado que los coeficientes del 
# denominador son a = 1, EL NUMERADOR HACE REFERENCIA A.....
# Al usar la rutina lfilter, la señal resultante presenta el desfase correspondiente
# al inducido por el filtro, mientras que en la rutina filtfilt, este desfase 
# se neutraliza.
# Respeto al orden del filtro, puede considerarse adecuado ya que atenuo 
# de forma eficaz el ruido de la señal capturada

#%%
# Pasa bajas IIR

plt.figure()
plt.subplot(2,1,1)

ye_pasa_bajas_iir = signal.lfilter(pasa_bajas_iir[1],pasa_bajas_iir[0],ye)
plt.plot(n,ye)
plt.plot(n,ye_pasa_bajas_iir)
plt.title('Antes/Despues de filtrar Pasa bajas IIR')
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.legend(['Señal capturada','Señal filtrada (lfilt)'])
plt.grid()

plt.subplot(2,1,2)
ye_pasa_bajas_iir = signal.filtfilt(pasa_bajas_iir[1],pasa_bajas_iir[0],ye)
plt.plot(n,ye)
plt.plot(n,ye_pasa_bajas_iir)
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.legend(['Señal capturada','Señal filtrada (filtfilt)'])
plt.grid()

plt.tight_layout()

#¿Por qué se utiliza el numerador y denominador? ¿Es necesario cambiar el orden
# del filtro? En tal caso hágalo y analice.

# -La funcion de transferencia de los filtros IIR esta conformada por polos y
# ceros, por lo que se requiere de numerador y denominador para expresarla.
# - Sí es necesario, dado que con un orden 30, la señal se elimina por completo
# en la banda pasante

# Pasa Bajas IIR MODIFICADO
orden = 3
fc = 1.25 # Hz
fc_normalizada = fc/fnyq

# Coeficientes
b,a = signal.iirfilter(orden,fc_normalizada,btype='lowpass',output='ba')
pasa_bajas_iir = [a,b]

# Diagrama de Bode del filtro diseñado
bode(b,a,orden)

plt.figure()
plt.subplot(2,1,1)

ye_pasa_bajas_iir = signal.lfilter(pasa_bajas_iir[1],pasa_bajas_iir[0],ye)
plt.plot(n,ye)
plt.plot(n,ye_pasa_bajas_iir)
plt.title('Antes/Despues de filtrar Pasa bajas FIR')
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.legend(['Señal capturada','Señal filtrada (lfilt)'])
plt.grid()

plt.subplot(2,1,2)
ye_pasa_bajas_iir = signal.filtfilt(pasa_bajas_iir[1],pasa_bajas_iir[0],ye)
plt.plot(n,ye)
plt.plot(n,ye_pasa_bajas_iir)
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.legend(['Señal capturada','Señal filtrada (filtfilt)'])
plt.grid()

plt.tight_layout()

# El filtro pasa bajas IIR de orden 3, logró el mismo resultado que el pasa
# bajas FIR de orden 30

#%% 7) Aplicación: Filtro de ruida eléctrico para una señal cargada
import scipy.signal as pds
#%% Señal cargada
fs = 500
fnyq = fs/2
senal = np.loadtxt('senal_filtros.txt')
#%%
f, t, Zxx = pds.stft(senal,fs, nperseg = 1000)
Zxxx = np.concatenate((Zxx[0],Zxx[1],Zxx[2]))
plt.pcolormesh(t, f, np.abs(Zxxx), vmin=0)

#%%
senal = np.transpose(senal)
senal = senal[0,:]

plt.figure()
plt.plot(senal)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.title('Señal Cargada')
plt.grid()

#%% Espectro de la señal cargada
f, Pxx = pds.welch(senal, fs, 'hanning', fs*2, fs)

plt.figure()
plt.semilogy(f, Pxx)
plt.xlabel('Frecuencia')
plt.ylabel('Amplitud')
plt.title('Espectro Señal Cargada')
plt.grid()

#%% Eliminación del ruido eléctrico de 60 Hz y de los alias de la señal
# Filtro Pasa bajas FIR
orden = 100
fc = 55 # Hz
fc_normalizada = fc/fnyq

# Coeficientes
a = 1
b = signal.firwin(orden+1,fc_normalizada,window='hamming',pass_zero='lowpass')
pasa_bajas_fir = [a,b]

# Diagrama de Bode del filtro diseñado
bode(b,a,orden)

#%% Rutina de filtrado
senalFiltrada = signal.filtfilt(pasa_bajas_fir[1],pasa_bajas_fir[0],senal)

plt.figure()
plt.plot(senalFiltrada)
plt.xlabel('Muestras')
plt.ylabel('Amplitud [mV]')
plt.title('Señal Filtrada por Pasa Banda FIR')
plt.grid()

#%% Espectro de la señal filtrada
f, Pxx = pds.welch(senalFiltrada, fs, 'hanning', fs*2, fs)

plt.figure()
plt.semilogy(f, Pxx)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.title('Espectro Señal Filtrada')
plt.grid()

#%% Comparación
plt.figure()
plt.plot(senal)
plt.plot(senalFiltrada)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.title('Comparación')
plt.legend(['Señal Cargada','Señal Filtrada'])
plt.xlim(100,1000)
plt.grid()
#%%
# Conclusiónes: 
    
# FILTROS IIR
# Pasa Bajas/Altas
# -ordenes elevados, distorsiona la señal, induce muchos desfase
# -Aumentar el orden, aumenta la pendiente de ateuacion
# -Logran el mismo efecto que los FIR con menor orden

# Pasa Banda
# -A medida que se aumenta el orden del filtro, se pierde el efecto deseado
# -sin embargo, si el orden es muy bajo, la pendiente de atenuación tambien
# es baja
# -A medida que se aumenta la frecuencia de la señal registrada, aumenta 
# la frecuencia de nyquist, esto obliga a que el diseño del filtro tenga
# un orden mas elevado para filtrar un rango determinado
# -Aumentar el orden del filtro aumenta la atenuación en la banda de rechazo

# Señal Cargada
# -Desconocer la procedencia de la señal, dificulta la etapa de filtrado,
# en la cual no se logra identificar a ciencia cierta que es ruido, y que no.

# Rechaza Banda
# - Si desea eliminarse un rango muy estrecho de frecuencia (factor de calidad)
# elevado como es conocido en el mundo analógico, debe incrementarse
# sustancialmente el orden del filtro




