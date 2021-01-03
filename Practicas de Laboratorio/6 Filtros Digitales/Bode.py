# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:09:13 2020

@author: SANTIAGO
"""

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Para ver el rango de freq total, ingresar fnyq, de lo contrario, se presenta
# normalizada entre 0 y 1

def bode(b,a,orden,fnyq = 1): 
    w,h = signal.freqz(b,a);

    FreqNormalizada = (w/max(w))*fnyq 
    magnitud = abs(h)
    magnitud_dB = 20 * np.log10 (magnitud)
    fase = np.unwrap(np.arctan2(np.imag(h),np.real(h)))
    
    plt.figure()
    plt.plot(FreqNormalizada,magnitud)
    plt.title('Filtro generado, Orden '  + str(orden) + ' - Magnitud')                                    
    plt.xlabel('Frequencia Normalizada')
    plt.ylabel('Amplitud')
    plt.grid()
    plt.tight_layout()
    
    plt.figure()
    plt.plot(FreqNormalizada,magnitud_dB)
    plt.title('Filtro generado, Orden '  + str(orden) + ' - Magnitud [dB]')                                    
    plt.xlabel('Frequencia Normalizada')
    plt.ylabel('Amplitud [dB]')
    plt.grid()
    plt.tight_layout()
    
    plt.figure()
    plt.plot(FreqNormalizada,fase)
    plt.title('Filtro generado, Orden '  + str(orden) + ' - Fase [pi-rad/muestras]')                               
    plt.xlabel('Frequencia Normalizada')
    plt.ylabel('Fase [pi-rad/muestras]')
    plt.grid()
    plt.tight_layout()