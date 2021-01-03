# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 19:07:46 2020

@author: USER
"""

import matplotlib.pyplot as plt;
import numpy as np;

#%%
'''
1. Implementacion de funciones discretas
1.a Impulso Unitario
'''

def impseq(n0,n1,n2):
    '''
    Recibe:
        n0: Punto donde inician las muestras
        n1: Inicio del vector de muestreo deseado
        n2: Final del vector de muestreo deseado
    Genera:
        n: Genera vector de muestras en el rango n1:n2, donde n0 
           marca el inicio de la señal
        y: Datos de cada muestra
    '''
    n = np.arange(n1,n2+1); # Se crea el vector de muestras
    y = (n-n0) == 0;        # y = true cuando se cumpla la condicion dentro
    return [n,y];           # del vector de muestreo.

'''
1.b Escalon 
'''

def escseq(n0,n1,n2):
    '''
    Recibe:
        n0: Punto donde inician las muestras
        n1: Inicio del vector de muestreo deseado
        n2: Final del vector de muestreo deseado
    Genera:
        n: Genera vector de muestras en el rango n1:n2, donde n0 
           marca el inicio de la señal
        y: Datos de cada muestra
    '''
    n = np.arange(n1,n2+1); # Se crea el vector de muestras
    y = (n-n0) >= 0;        # y = true cuando se cumpla la condicion dentro
    return [n,y];           # del vector de muestreo.

'''
1.c Rampa 
'''

def rampseq(n0,n1,n2):
    '''
    Recibe:
        n0: Punto donde inician las muestras
        n1: Inicio del vector de muestreo deseado
        n2: Final del vector de muestreo deseado
    Genera:
        n: Genera vector de muestras en el rango n1:n2, donde n0 
           marca el inicio de la señal
        y: Datos de cada muestra
    '''
    #j=0;
    y=[];
    n = np.arange(n1,n2+1);         # Se crea el vector de muestras
    for i in range(0,len(n)):       # Una variable recorre el vector de muestreo
        if (n[i]-n0) < 0:           # Si se cumple esta condificon
            y.insert(i,0);          # al vector Y se le inserta un 0 
        else:
            y.insert(i,n[i]-n0)   # De lo contrario se le inserta
                                    # el valor de n[i]-n0
    return [n,y];   

#%%  
'''
Las funciones creadas son llamadas y posteriormente graficadas individualmente
'''
impulso=impseq(0,-10,10);         
escalon=escseq(0,-10,10);
rampa=rampseq(0,-10,10);

print("\nFunción Impulso:");
fig1 = plt.figure();                          
plt.stem(impulso[0],impulso[1]);      
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("Impulso Discreto");
plt.grid();

print("\nFunción Escalón:");
fig2 = plt.figure();                          
plt.stem(escalon[0],escalon[1]);       
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("Escalón Discreto");
plt.grid();

print("\nFunción Rampa:");
fig3 = plt.figure();                          
plt.stem(rampa[0],rampa[1]);   
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("Rampa Discreta");
plt.grid();


#%%
'''
2. Genere las secuencias y grafique los resultados
2.a 
x1(n) = 5δ(n + 3) + 4δ(n + 2) + 3δ(n + 1) + 2δ(n) + δ(n).
¿Como debe ser el vector de muestras?
'''
x1_a = impseq(-3,-4,1);         # En x1_i retorna:
x1_b = impseq(-2,-4,1);         # [vector de muestras,
x1_c = impseq(-1,-4,1);         # impulso/true en la posicion deseada]
x1_d = impseq(0,-4,1);
x1_e = impseq(0,-4,1);
                                # Calculo de la señal x1
x1 = 5*x1_a[1] + 4*x1_b[1] + 3*x1_c[1] + 2*x1_d[1] + x1_e[1];
print('x1: ',x1);

fig4 = plt.figure();            # Grafica de la señal
plt.stem(np.arange(-4,2),x1);
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("x1 = 5δ(n + 3) + 4δ(n + 2) + 3δ(n + 1) + 2δ(n) + δ(n).");
plt.grid();

print("\nEl vector de muestras debe ser:\n"); 
print("- De igual cantidad de muestras de x(1)");
print("- Su valor inicial debe ser <= muestra mas adelantada -1");
print("- Su valor final debe ser >= muestra mas atrasada +1");

#%%
'''
2.b 
x2(n) = −2u(n + 5) + 4u(n),−5 ≤ n ≤ 5
'''
x2_a = escseq(-5,-5,5);         # En x2_i retorna lo mismo que en x1_i
x2_b = escseq(0,-5,5);
                                # Calculo de la señal x2
x2 = -2*x2_a[1] + 4*x2_b[1];
print('x2: ',x2);
                            
fig5 = plt.figure();            # Grafica de la señal
plt.stem(np.arange(-5,6),x2);
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("x2 = −2u(n + 5) + 4u(n),−5 ≤ n ≤ 5");
plt.grid();

#%%
'''
2.c
x3(n) = e0.05nsin(0.1πn) , 0 ≤ n ≤ 100. Comente acerca de la forma de onda.
'''
tiempo_x3 = np.linspace(0,100,100);                         # Vector de tiempo de muestreo
x3 = np.exp(0.05*tiempo_x3)*np.sin(0.1*np.pi*tiempo_x3);    # Calculo de la señal x3

fig6 = plt.figure();                                        # Grafica de la señal
plt.stem(tiempo_x3,x3);
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("x3(n) = e0.05nsin(0.1πn) , 0 ≤ n ≤ 100");
plt.grid();

'''
La forma de onda graficada, incrementa su amplitud gradualmente con el 
incremento del tiempo, hecho que se atribuye al factor positivo al que esta 
elevado (e), pues teóricamente causa una amplificacion de la señal, y al estar 
en forma de producto con el vector de muestras, es notorio como el escalar 
resultante que multiplica a la señal seno, genera su amplificacion en el tiempo.
'''

#%%
'''
2.d
x4(n) = r(n + 2) − r(n − 2) − 4u(n − 5),−5 ≤ n ≤ 10
'''

x4_a = rampseq(-2,-5,10);
x4_b = rampseq(2,-5,10);
x4_c = rampseq(5,-5,10);

# Para realizar las restas, deben operarse arreglos, por lo que se emplea
# np.asarray, para transformar listas, en arreglos.
x4 = np.asarray(x4_a[1]) - np.asarray(x4_b[1]) - 4*np.asarray(x4_c[1]);

fig7 = plt.figure();            # Grafica de la señal
plt.stem(x4_a[0],x4);
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("x4(n) = r(n + 2) − r(n − 2) − 4u(n − 5),−5 ≤ n ≤ 10");
plt.grid();

#%%
'''
3. Genere las secuencias y grafique los resultados
Sea 𝑥(𝑛) = {−4, −3, −2, −1,0, 1̂, 2,3,4}. Genere las siguientes 
secuencias y grafique losresultados.
3.a 𝑥5(𝑛) = 2𝑥(𝑛 − 4) + x(n)

Dado que se tiene el vector de datos para cada muestra, 
pero no su correspondiente vector de tiempo, debe crearse de 
tal forma que la muestra inicial este en 1^: 
'''
xn5 = np.arange(-4,5,1);                        # Vector de datos
xn5_atrasada = np.append(np.zeros(4),xn5);    # Vector de datos adelantado
xn5_acomodada = np.append(xn5,np.zeros(4));     # vector original acomodado a la longitud de xn5_atrasada

n5 = np.arange(-5,8,1);                         # Vector de muestreo resultante
xn5 = 2*xn5_atrasada + xn5_acomodada;         # Calculo de nx5

fig8=plt.figure();                              # Grafica
plt.stem(n5,xn5);
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("x(n5) = 2x(n-4) + x(n)");
plt.grid();

#%%
'''
3.b. 𝑥6(𝑛) =2𝑒0.5𝑛𝑥(𝑛) + 𝑠𝑖𝑛(0.2𝜋𝑛) 𝑥(𝑛 + 2), −20 ≤ 𝑛 ≤ 20
'''
xn6 = np.arange(-4,5,1);                                            # Vector de datos inicial
xn6_ajustada = np.append(np.zeros(15),xn6);                         # Datos ajustados al rango de acotacion
xn6_ajustada = np.append(xn6_ajustada,np.zeros(17));                # se agregaron ceros al inicio y al final

xn6_adelantada = np.append(np.zeros(13),xn6);                       # Para el calculo se requeria adelantar la
xn6_adelantada = np.append(xn6_adelantada,np.zeros(19));            # señal en 2 muestras

xn6_a = 2*np.exp(0.5*xn6_ajustada);                                 # Calculos de cada termino de xn6
xn6_b = np.multiply(np.sin(0.2*np.pi*xn6_ajustada),xn6_adelantada);

xn6 = xn6_a + xn6_b;                                                # Calculo de xn6

fig8=plt.figure();                                                   # Grafica
plt.stem(np.arange(-20,21,1),xn6);
plt.xlabel("Tiempo");
plt.ylabel("Amplitud");
plt.title("x6(n) = 2e(0.5n) + sin(0.2*pi*n)*x(n+2),-20<=n<=20");
plt.grid();



