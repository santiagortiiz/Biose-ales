#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:49:59 2020

@author: santiago Cardona Flórez
         Santiago Ortíz Ceballos
"""

import numpy as np;
import matplotlib.pyplot as plt;

#%% Punto 0

def impseq(n0,n1,n2):
    # Genera x(n) = delta(n-n0); n1 <= n <= n2
    # ----------------------------------------------
    n = np.arange(n1,n2+1); # Se crea el vector de muestras
    x = (n-n0) == 0;
    return [n,x]
   
fig1 = plt.figure()
v = impseq(0,-10,10)
plt.stem(v[0],v[1])
plt.title('Funcion Impulso');plt.ylabel('Amplitud');plt.xlabel('Tiempo (s)')

#%% Punto 1

''' Implemente una función en Python que permita generar una función escalón 
    unitario, definida en un intervalo 𝑛1≤𝑛0≤n2  
'''
def escseq(n0,n1,n2):
    '''
    n0: inicio de la función escalón 
    n1: inicio del vector de muestras
    n2: fin del vector de muestras
'''
    n = np.arange(n1,n2+1); # Se crea el vector de muestras
    x = (n-n0) >= 0;
    return [n,x]

fig2 = plt.figure()
w = escseq(0,-10,10)
plt.stem(w[0],w[1])
plt.title('Funcion Escalon');plt.ylabel('Amplitud');plt.xlabel('Tiempo (s)')

#%% Punto 2 

''' Implemente una función en Python que permita generar una función rampa,
    definida en un intervalo 𝑛1≤𝑛0≤n2  
''' 
def ramseq(n0,n1,n2):
    '''
    n0: inicio de la función rampa 
    n1: inicio del vector de muestras
    n2: fin del vector de muestras
'''
    n = np.arange(n1,n2+1); # Se crea el vector de muestras
    x = np.arange(n1,n2+1); # Se crea el vector valores
    for i in np.arange(len(n)):
        if x[i] < n0:
            x[i]= False
        else:
            x[i] = x[i] - n0
    return [n,x]
 
fig3 = plt.figure()
x = ramseq(-7,-10,10)
plt.stem(x[0],x[1])
plt.title('Funcion Rampa');plt.ylabel('Amplitud');plt.xlabel('Tiempo (s)')

#%% Punto 3

''' Genere las siguientes secuencias usando las funciones básicas de Python 
    que se han presentado. Grafique los resultados.
    '''
# inciso a

delta1 = impseq(-3,-15,15) # 𝛿(𝑛+3)  
delta2 = impseq(-2,-15,15) # 𝛿(𝑛+2)  
delta3 = impseq(-1,-15,15) # 𝛿(𝑛+1)  
delta4 = impseq(0,-15,15) # 𝛿(𝑛)  

x1 = 5*delta1[1] + 4*delta2[1] + 3*delta3[1] + 2*delta4[1] + delta4[1]
fig6 = plt.figure()
plt.stem(delta1[0],x1)
plt.title('Funcion X1(n)');plt.ylabel('Amplitud');plt.xlabel('Muestra (n)')    
    
# inciso b

u1 =  escseq(-5,-10,10) # 𝑢(𝑛+5)  
u2 =  escseq(0,-10,10) # 𝑢(𝑛)  

x2 =  (-2)*u1[1] + 4*u2[1]   
fig7 = plt.figure()
plt.stem(u1[0],x2)
plt.title('Funcion X2(n)');plt.ylabel('Amplitud');plt.xlabel('Muestra (n)')        
    
# inciso c

n = np.linspace(0,31.5/(0.1*np.pi),100)
x3 = np.exp(0.05*n)*np.sin(0.1*np.pi*n)  
fig8 = plt.figure()
plt.stem(n,x3)
plt.title('Funcion X3(n)');plt.ylabel('Amplitud');plt.xlabel('Muestra (n)')       
    
# inciso d

r1 = ramseq(-2,-5,10)  #  𝑟(𝑛+2)  
r2 = ramseq(2,-5,10) #  𝑟(𝑛-2)  
u1 = escseq(5,-5,10) #  𝑢(𝑛−5)  

x4 = r1[1] - r2[1] - 4*u1[1]
fig9 = plt.figure()
plt.stem(r1[0],x4)
plt.title('Funcion X4(n)');plt.ylabel('Amplitud');plt.xlabel('Muestra (n)')
    
    
#%% Punto 4 

'''  Sea 𝑥(𝑛) = {−4, −3, −2, −1,0, 1̂, 2,3,4}. Genere las siguientes secuencias  
     y grafique los resultados.  
'''
xn = np.arange(-4,5)  # creación vector 𝑥(𝑛) = {−4, −3, −2, −1,0, 1̂, 2,3,4}  
n = np.arange(-5,8)   # creación del vector de muestras con el cero en 1̂ 

# inciso a

x5 = 2*(np.concatenate(([0,0,0,0],xn),axis=None)) + np.concatenate((xn,[0,0,0,0]),axis=None)
fig10 = plt.figure()
plt.stem(n,x5)
plt.title('Funcion X5(n)');plt.ylabel('Amplitud');plt.xlabel('Muestra (n)')  
    #%%
# inciso b

x6 = 2*np.exp(0.5*n)*xn + np.sin(0.2*np.pi*n)*(xn+2)
fig11 = plt.figure()
plt.stem(n,x6)
plt.title('Funcion X6(n)');plt.ylabel('Amplitud');plt.xlabel('Muestra (n)')     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
plt.show()