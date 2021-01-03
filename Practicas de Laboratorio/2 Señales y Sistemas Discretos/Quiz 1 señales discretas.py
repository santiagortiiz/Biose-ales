# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""
import numpy as np;
import matplotlib.pyplot as plt;

'''
Corrección: Funcion para igualar tamaños de muestreo y operar funciones
'''
def IgualarVectores(origen1,vector1,origen2,vector2):
    " Inicialmente se crean los vectores de muestreo en funcion del origen ingresado "
    
    " Para el Vector 1 "
    vectorMuestreo_1 = np.arange(-len(vector1[vector1-origen1 < 0]),len(vector1-origen1>0)+1,1);
                                                                            
    " Para el Vector 2 "
    vectorMuestreo_2 = np.arange(-len(vector2[vector2-origen2 < 0]),len(vector2-origen2>0)+1,1);
    
    " Vector de muestreo comun "
    minimoEntreVectores = np.array([min(vectorMuestreo_1),min(vectorMuestreo_2)]);
    maximoEntreVectores = np.array([max(vectorMuestreo_1),max(vectorMuestreo_2)]);
    vectorMuestraComun = np.arange(min(minimoEntreVectores),max(maximoEntreVectores)+1,1);
    
    " Completando Vectores de datos (vector 1 y vector 2)"
    if min(vectorMuestreo_1) < min(vectorMuestreo_2):
        cantidadZeros1 = abs(min(vectorMuestreo_1) - min(vectorMuestreo_2));
        vector2 = np.append(np.zeros(cantidadZeros1),vector2);
    elif  min(vectorMuestreo_1) > min(vectorMuestreo_2):
        cantidadZeros1 = abs(min(vectorMuestreo_1) - min(vectorMuestreo_2));
        vector1 = vector1=np.append(np.zeros(cantidadZeros1),vector1);
            
    if max(vectorMuestreo_1) < max(vectorMuestreo_2):
        cantidadZeros2 = abs(max(vectorMuestreo_1) - max(vectorMuestreo_2));
        vector2 = np.append(np.zeros(vector2,cantidadZeros2));
    elif  max(vectorMuestreo_1) > max(vectorMuestreo_2):
        cantidadZeros2 = abs(max(vectorMuestreo_1) - max(vectorMuestreo_2));
        vector1 = np.append(np.zeros(vector1,cantidadZeros2));    

    print("\nLongitud vector 1: ",len(vector1));                            
    print("Longitud vector de muestras 1: ",len(vectorMuestreo_1));  
    print("\nLongitud vector 2: ",len(vector2));                            
    print("Longitud vector de muestras 2: ",len(vectorMuestreo_2));

    print("\n\nMinimo entre vectores :",minimoEntreVectores);
    print("Maximo entre vectores :",maximoEntreVectores);
    print("Longitud del vector de muestras comun :",vectorMuestraComun);  
    
    return [vectorMuestraComun,vector1,vector2];

" CORREGIR!! NO DEBE HACERSE CON MAXIMOS, TIENE QUE CONTAR DIFERENCIA DE TAMAÑOS/POSICIONES
         
#%%
a=np.arange(-3,4,1);
b=np.arange(-5,2,1);
c=IgualarVectores(2,a,1,b);






#%%
# 1 fumcion sum_sen

def sum_sen(muestras,vector1,vector2):
    y = vector1 + vector2;
    
    plt.figure();                                   
    plt.stem(muestras,y);
    plt.xlabel("Tiempo");
    plt.ylabel("Amplitud");
    plt.grid();

#%%%
# 2 funciones
    
# a) x1(n1) = sin(0.01 PI n1) ,-10 < n < 10
n1 = np.arange(-10,11,1);
n1 = np.append(n1,np.zeros(5));
x1 = np.sin(0.01*np.pi*n1);

#%%
# b) x2(n2) = 5e0.1n2, -5 < n2 < 15
n2 = np.arange(-5,16,1);
n2 = np.append(np.zeros(5),n2);
x2 = 5*np.exp(0.1*n2);

#%%
# c) x3(n3) = {-3,-2,-1^,0,1,2,3,4,5}
x3 = np.arange(-2,7,1);
x3 = np.append(np.zeros(8),x3);
x3 = np.append(x3,np.zeros(9));

#%%
# d) y(n)= x1 + x2 + x3
n4 = np.arange(-10,16);
x4 = x1 + x2 + x3;

'''
Solo debe ingresarse 1 vector de muestra ya que estan igualados en longitud
'''
sum_sen(n1,x1,x1);
sum_sen(n1,x2,x2);
sum_sen(n1,x3,x3);
sum_sen(n1,x4,x4);





