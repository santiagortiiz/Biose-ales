# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 10:05:39 2020

@author: USER
"""

'''
e) Análisis estadística para 15 ciclos ECG de la señal filtrada

fig3,ax = plt.subplots(3,1);                                                    # Se crea la figura contenedora
ax[0].plot(QuinceTiempos[:,0],QuinceCiclos[:,0]);                               # Se grafican las señales                                         
ax[1].plot(QuinceTiempos[:,1],QuinceCiclos[:,1]);
ax[2].plot(QuinceTiempos[:,2],QuinceCiclos[:,2]); 
fig3.tight_layout();

fig4,ax = plt.subplots(3,1);                                                    # Se crea la figura contenedora
ax[0].plot(QuinceTiempos[:,3],QuinceCiclos[:,3]);                               # Se grafican las señales                                         
ax[1].plot(QuinceTiempos[:,4],QuinceCiclos[:,4]);
ax[2].plot(QuinceTiempos[:,5],QuinceCiclos[:,5]); 
fig4.tight_layout();

fig5,ax = plt.subplots(3,1);                                                    # Se crea la figura contenedora
ax[0].plot(QuinceTiempos[:,6],QuinceCiclos[:,6]);                               # Se grafican las señales                                         
ax[1].plot(QuinceTiempos[:,7],QuinceCiclos[:,7]);
ax[2].plot(QuinceTiempos[:,8],QuinceCiclos[:,8]); 
fig5.tight_layout();

fig6,ax = plt.subplots(3,1);                                                    # Se crea la figura contenedora
ax[0].plot(QuinceTiempos[:,9],QuinceCiclos[:,9]);                               # Se grafican las señales                                         
ax[1].plot(QuinceTiempos[:,10],QuinceCiclos[:,10]);
ax[2].plot(QuinceTiempos[:,11],QuinceCiclos[:,11]); 
fig6.tight_layout();

fig7,ax = plt.subplots(3,1);                                                    # Se crea la figura contenedora
ax[0].plot(QuinceTiempos[:,12],QuinceCiclos[:,12]);                               # Se grafican las señales                                         
ax[1].plot(QuinceTiempos[:,13],QuinceCiclos[:,13]);
ax[2].plot(QuinceTiempos[:,14],QuinceCiclos[:,14]); 
fig7.tight_layout();

fig8,ax = plt.subplots(3,1);                                                    # Se crea la figura contenedora
ax[0].plot(QuinceTiempos[:,0],QuinceCiclos[:,0]);                               # Se grafican las señales                                         
ax[1].plot(QuinceTiempos[:,1],QuinceCiclos[:,1]);
ax[2].plot(QuinceTiempos[:,2],QuinceCiclos[:,2]); 
fig8.tight_layout();

'''

#%%
''' 3. c) Análisis a 1 tramo filtrado de contraccion de cada músculo


OPCION 1

x_min = int(0*Fs);
x_max = int(2.5*Fs);
tiempoCicloEMG = tiempo_EMG[x_min:x_max];  

cicloEMG_triceps_original = senalEMG_triceps_original[x_min:x_max];             # Se establece el intervalo 
cicloEMG_triceps_filtrada = senalEMG_triceps_filtrada[x_min:x_max];             # de 1 ciclo de EMG triceps

cicloEMG_biceps_original = senalEMG_biceps_original[x_min:x_max];               # Se establece el intervalo 
cicloEMG_biceps_filtrada = senalEMG_biceps_filtrada[x_min:x_max];               # de 1 ciclo de EMG biceps

fig9,ax = plt.subplots(1,2);                                                        # Se crea la figura contenedora

ax[0].plot(tiempoCicloEMG,cicloEMG_triceps_original);ax[0].grid();                  # Se grafican las señales                                         
ax[0].plot(tiempoCicloEMG,cicloEMG_triceps_filtrada);
ax[1].plot(tiempoCicloEMG,cicloEMG_biceps_original);ax[1].grid();                                                                     
ax[1].plot(tiempoCicloEMG,cicloEMG_biceps_filtrada);

ax[0].set_ylabel("Voltaje [uV]");                                               # Se referencian los ejes
ax[0].set_xlabel("Tiempo [s]");                                               
ax[1].set_xlabel("Tiempo [s]");

ax[0].set_title("Ciclo EMG Triceps");                                           # Se referencias las graficas
ax[1].set_title("Ciclo EMG Biceps");
ax[0].legend(["Señal Original","Señal Filtrada"]);
ax[1].legend(["Señal Original","Señal Filtrada"]);

fig9.tight_layout();



OPCION 2

x_min = int(0*Fs);
x_max = int(2.5*Fs);
tiempoCicloEMG = tiempo_EMG[x_min:x_max];  

cicloEMG_triceps_original = senalEMG_triceps_original[x_min:x_max];             # Se establece el intervalo 
cicloEMG_triceps_filtrada = senalEMG_triceps_filtrada[x_min:x_max];             # de 1 ciclo

fig9 = plt.figure();                                                            # Se crea la figura contenedora
ax_fig9 = plt.axes();

ax_fig9.plot(tiempoCicloEMG,cicloEMG_triceps_original);                         # Se grafica la señal
ax_fig9.plot(tiempoCicloEMG,cicloEMG_triceps_filtrada);                         # Se grafica la señal

ax_fig9.set_xlabel("Tiempo [s]");                                               # Se referencia la grafica
ax_fig9.set_ylabel("Voltaje [uV]");
ax_fig9.set_title("Ciclo EMG Triceps");
ax_fig9.legend(["Señal Original","Señal Filtrada"]);
ax_fig9.grid();

fig9.tight_layout();


cicloEMG_biceps_original = senalEMG_biceps_original[x_min:x_max];             # Se establece el intervalo 
cicloEMG_biceps_filtrada = senalEMG_biceps_filtrada[x_min:x_max];             # de 1 ciclo

fig10 = plt.figure();                                                            # Se crea la figura contenedora
ax_fig10 = plt.axes();

ax_fig10.plot(tiempoCicloEMG,cicloEMG_biceps_original);                         # Se grafica la señal
ax_fig10.plot(tiempoCicloEMG,cicloEMG_biceps_filtrada);                         # Se grafica la señal

ax_fig10.set_xlabel("Tiempo [s]");                                               # Se referencia la grafica
ax_fig10.set_ylabel("Voltaje [uV]");
ax_fig10.set_title("Ciclo EMG Biceps");
ax_fig10.legend(["Señal Original","Señal Filtrada"]);
ax_fig10.grid();

fig10.tight_layout();
'''
#%%
'''d) Promedio y varianza para cada tramo de la señal filtrada EMG del biceps y triceps
for i in range(10):                                                             # En cada columna de las matricez, 
    DiezCiclos[:,i] = senalEMG_triceps_filtrada[x_min:x_max];                   # se inserta un ciclo de la 
    DiezTiempos[:,i] = tiempoEMG[x_min:x_max];                                  # señal filtrada de ECG y su 
    x_min = x_min + muestras_por_ciclo_triceps;                                 # respectivo intervalo de tiempo
    x_max = x_max + muestras_por_ciclo_triceps;
   
#%%
fig11,ax = plt.subplots(3,2);                                                    # Se crean las figuras contenedoras

ax[0,0].plot(DiezTiempos[:,0],DiezCiclos[:,0]);ax[0,0].grid();              # Se grafican las señales                                         
ax[1,0].plot(DiezTiempos[:,1],DiezCiclos[:,1]);ax[1,0].grid(); 
ax[2,0].plot(DiezTiempos[:,2],DiezCiclos[:,2]);ax[2,0].grid();  
ax[0,1].plot(DiezTiempos[:,3],DiezCiclos[:,3]);ax[0,1].grid();                                                                     
ax[1,1].plot(DiezTiempos[:,4],DiezCiclos[:,4]);ax[1,1].grid(); 
ax[2,1].plot(DiezTiempos[:,5],DiezCiclos[:,5]);ax[2,1].grid();  
                                                  
ax[2,0].set_xlabel('tiempo [s]');                                               # Se referencian los ejes
ax[2,1].set_xlabel('tiempo [s]');
ax[0,0].set_ylabel('Voltaje [uV]');
ax[1,0].set_ylabel('Voltaje [uV]');
ax[2,0].set_ylabel('Voltaje [uV]');

ax[0,0].legend(['1 Ciclo']);                                                    # Se referencian las graficas
ax[1,0].legend(['2 Ciclo']);
ax[2,0].legend(['3 Ciclo']);
ax[0,1].legend(['4 Ciclo']);
ax[1,1].legend(['5 Ciclo']);
ax[2,1].legend(['6 Ciclo']);

fig11.tight_layout();    

#%%
fig12,ax = plt.subplots(2,2);                                                    # Se crean las figuras contenedoras

ax[0,0].plot(DiezTiempos[:,6],DiezCiclos[:,6]);ax[0,0].grid();              # Se grafican las señales                                         
ax[1,0].plot(DiezTiempos[:,7],DiezCiclos[:,7]);ax[1,0].grid(); 
ax[0,1].plot(DiezTiempos[:,8],DiezCiclos[:,8]);ax[0,1].grid();  
ax[1,1].plot(DiezTiempos[:,9],DiezCiclos[:,9]);ax[1,1].grid();    
                                                  
ax[1,0].set_xlabel('tiempo [s]');                                               # Se referencian los ejes
ax[1,1].set_xlabel('tiempo [s]');
ax[0,0].set_ylabel('Voltaje [uV]');
ax[1,0].set_ylabel('Voltaje [uV]');

ax[0,0].legend(['7 Ciclo']);                                                    # Se referencian las graficas
ax[1,0].legend(['8 Ciclo']);
ax[0,1].legend(['9 Ciclo']);
ax[1,1].legend(['10 Ciclo']);

fig12.tight_layout();    
'''
#%%
'''d) Promedio y varianza para cada tramo de la señal filtrada EMG del biceps y triceps
x_min = [0, 2.6, 5.55, 8.5, 11.5, 14.5, 17.6, 21, 25, 28.8];
x_max = [2.6, 5.4, 8.3, 11.2, 14, 17.5, 20.5, 25, 28.5, 30];

DiezCiclos = np.zeros((muestras_por_ciclo_triceps,10));
DiezTiempos = np.zeros((muestras_por_ciclo_triceps,10)); 

for i in range(10):                                                             # En cada columna de las matricez, 
    DiezCiclos[:,i] = senalEMG_triceps_filtrada[int(Fs*x_min[i]):int(Fs*x_max[i])];                   # se inserta un ciclo de la 
    DiezTiempos[:,i] = tiempoEMG[int(Fs*x_min[i]):int(Fs*x_max[i])];  
    '''



