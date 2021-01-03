# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:45:20 2020

@author: Santiago Ortiz - Santiago Cardona
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio;

#%%
# 4) APLICATIVO

# 4.1) Cree una señal que sea la suma de tres componentes sinusoidales con frecuencias de 60,
# 120 y 360 Hz. Defina la frecuencia de muestreo mínima necesaria para representar la señal,
# y utilice la frecuencia de muestreo necesaria para representarla.

f1 = 60     # Frecuencias Fundamentales
f2 = 120
f3 = 360
fs = 7200   # Frecuencia de muestreo 10*2Fs

T1 = 1/f1
T2 = 1/f2
T3 = 1/f3
Ts = 1/fs   # Período de muestreo

t1 = np.arange(0, T1+Ts, Ts)    # Vectores de tiempo de cada señal   
t2 = np.arange(0, T2+Ts, Ts)
t3 = np.arange(0, T3+Ts, Ts)
ts = np.arange(0, T1 + Ts, Ts)       # Vector de tiempo común

senal_1 = np.sin(2*np.pi*f1*ts)     # Componentes de la señal
senal_2 = np.sin(2*np.pi*f2*ts)
senal_3 = np.sin(2*np.pi*f3*ts)

senal_compuesta = senal_1 + senal_2 + senal_3   # Señal compuesta

fig1 = plt.figure();    # Gráfica
plt.plot(ts,senal_1)
plt.plot(ts,senal_2)
plt.plot(ts,senal_3)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend(['60Hz','120Hz','360Hz'])
plt.grid();

fig2 = plt.figure();    # Gráfica
plt.plot(ts,senal_compuesta)
plt.title('Senosoidal con ruido')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()

#%%
# 4.2) Calcule la transformada de Fourier de la señal y grafique el espectro de frecuencia.
# Identifique en el espectro las frecuencias que componen la señal (trabaje con 10 ciclos de
# la señal).

# Construccion de 10 ciclos de la señal compuesta
ts_10 = np.arange(0, 10*T1 + Ts, Ts)

senal_1 = np.sin(2*np.pi*f1*ts_10)     
senal_2 = np.sin(2*np.pi*f2*ts_10)
senal_3 = np.sin(2*np.pi*f3*ts_10)

señal_10_ciclos = senal_1 + senal_2 + senal_3

fig3 = plt.figure();    # Gráfica
plt.plot(ts_10,señal_10_ciclos)
plt.title('10 ciclos Senosoidal con ruido')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud ')
plt.grid();

# Transformada de Fourier de dicha señal
SEÑAL_10_CICLOS = np.abs(np.fft.fft(señal_10_ciclos))

N = SEÑAL_10_CICLOS.shape[0]
F = np.arange(0,N)*fs/N

fig4 = plt.figure();    # Gráfica
plt.plot(F[(F > 20) & (F < 400)],SEÑAL_10_CICLOS[(F > 20) & (F < 400)])
plt.title('Espectro de frecuencias')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud (V)')
plt.grid();

#%%
# 4.3) Consulte la función que permite realizar el cálculo de la transformada inversa de .
# Fourier Aplíquelo a la señal anterior.

senal_reconstruida = np.fft.ifft(SEÑAL_10_CICLOS)
fig5 = plt.figure();    # Gráfica
plt.plot(ts_10,senal_reconstruida.real)
plt.title('Transformada inversa de Fourier')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (V)')
plt.grid();

#%%
# 4.4) ¿Podría decir que las siguientes líneas aplican un filtro? ¿Por qué?
# Extraiga de manera similar cada una de las componentes de la señal.

F1 = np.fft.fft(señal_10_ciclos);
print('\nF1:')
print(F1)
F2 = np.zeros((len(F1)));
print('\nF2:')
print(F2)

#F2[9:13] = F1[9:13]
F2[20:21] = F1[20:21]
print('\nF2 luego de asignar F1[9:13]:')
print(F2)

xr = np.fft.ifft(F2)

fig6 = plt.figure();    # Gráfica
plt.plot(ts_10,np.real(xr))
plt.title('Señal luego de aplicar el algoritmo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (V)')
plt.grid();

# Transformada de Fourier de dicha señal
SENAL_FILTRADA = np.abs(np.fft.fft(xr))

N = SENAL_FILTRADA.shape[0]
F = np.arange(0,N)*fs/N

fig7 = plt.figure();    # Gráfica
plt.plot(F[(F > 20) & (F < 400)],SENAL_FILTRADA[(F > 20) & (F < 400)])
plt.title('Espectro de frecuencias luego de aplicar el algoritmo')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud (V)')
plt.grid();

# Análisis:
# Efectivamente, el algoritmo aplicado puede ser considerado un filtro, ya que 
# eliminó 2 de las 3 componentes, dejando la menor de ellas, como si de un filtro
# pasa bajas se tratase

#%%
# 4.5 El archivo adjunto (senecg.mat) contiene una señal de ECG adquirida a una 
# frecuencia de muestreo de 250 Hz. Realice un análisis de la señal y determine si
# es necesario eliminar ruido, en tal caso, elimínelo y compruebe que lo haya 
# realizado (calcule la transformada inversa de Fourier de la señal filtrada).

mat_contents = sio.loadmat('senecg.mat')                                      
                                                                                # Inicialmente se carga la señal en formato matlab
print("Las claves cargadas fueron: " + str(mat_contents.keys()))                # y se muestra el formato en el cual estan registrados
senal_ECG = np.squeeze(mat_contents['ECG'])                                     # los datos

fs = 250
tiempo_ECG = np.arange( 0, len(senal_ECG)/fs, 1/fs);    # Vector de tiempo generado

fig8 = plt.figure();    # Gráfica de la señal cargada
plt.plot(tiempo_ECG,senal_ECG)
plt.title('Señal ECG cargada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud(V)')
plt.grid();

fig9 = plt.figure();    # Gráfica de un ciclo tomado del centro para garantizar la totalidad de la señal 
plt.plot(tiempo_ECG[(tiempo_ECG > 1.7) & (tiempo_ECG < 2.6)],   # y considerando que teóricamente tiene duracion de 0.9s
                    senal_ECG[(tiempo_ECG > 1.7) & (tiempo_ECG < 2.6)])
plt.title('1 Ciclo Señal ECG cargada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud(V)')
plt.grid();

# Espectro para la señal cargada
SENAL_ECG = np.abs(np.fft.fft(senal_ECG))

N = SENAL_ECG.shape[0]
F = np.arange(0,N)*fs/N

fig10 = plt.figure();    # Gráfica
plt.plot(F,SENAL_ECG)
plt.title('Espectro de frecuencias de la señal ECG cargada')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud (V)')
plt.grid();

# Algoritmo de filtrado
F1 = np.fft.fft(SENAL_ECG);
F2 = np.zeros((len(F1)));

# Eliminamos la frecuencia de 0Hz si esta presente que corresponde a un nivel DC
# y se toman frecuencias menores a 50Hz para evitar el ruido generado por la red
# eléctrica de 60Hz, y además se considera únicamente el espectro < 2fs para no
# tomar ningun alias del espectro original

F2[(F > 5) & (F < 50)] = F1[(F > 5) & (F < 50)]
F2[(F > 200) & (F < 250)] = F1[(F > 200) & (F < 250)] 

# Luego se reconstruye la señal con la transformada inversa
ECG_reconstruido = np.fft.ifft(F2)  

fig11 = plt.figure()    # Se grafica la señal reconstruida
plt.plot(tiempo_ECG,np.real(ECG_reconstruido))
plt.title('Señal luego de aplicar el algoritmo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (V)')
plt.grid();

# Transformada de Fourier de dicha señal
ECG_FILTRADO = np.abs(np.fft.fft(ECG_reconstruido))

N = ECG_FILTRADO.shape[0]
F = np.arange(0,N)*fs/N

fig12 = plt.figure()    # Finalmente se grafica el espectro de la señal reconstruida
plt.plot(F,ECG_FILTRADO)
plt.title('Espectro de frecuencias de la señal ECG luego de aplicar el algoritmo')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud (V)')
plt.grid();

# Análisis: mejorar!
# Este método de filtrado parece ideal dado que elimina por completo las frecuencias
# que no son de interés, sin embargo la señal reconstruida carece de la forma habitual
# de un ECG a pesar de contener las componentes frecuenciales típicas en el.

# Conclusiones:
# Es indispensable conocer el espectro de frecuencias de una señal fisiológico si 
# se va a analizar, dado que esto permite determinar componentes de ruido, y componentes
# propias de la señal, lo cual es de utilidad en caso de que se desee filtrar la señal

# Aplicar un filtro partiendo del espectro de frecuencias de la señal en el cual se
# eliminan componentes no deseadas y se reconstruye la señal con base al espectro 
# resultante, no es eficiente, ya que la señal original se ve afectada por el efecto
# inducido de este proceso, y no resulta una señal confiable
#%%
plt.show()
