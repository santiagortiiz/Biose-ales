# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:02:51 2020

@author: Santiagos
"""

import scipy.io as sio;                                                                     # Librerias necesarias para extraer informacion
from csv import reader as reader_csv;                                                       # de archivos .mat y .txt

import numpy as np;
import math;
#%%
class Procesador(object):
    def __init__(self):                                                                     # Se inicializan los atributos que tendra el modelo 
        self.senal = np.asarray([]);                                                        # para realizar el procesamiento necesario para
        self.canalActual = -1;                                                              # la VISUALIZACION de la señal cargada.
        self.banderaDimension = 0;
        self.x_min = 0;
        self.x_max = 0;
        
#        self.senalDescompuesta = [];                                                       # Se inicializan los atributos necesarios para 
        self.nivel_max = 0;                                                                 # FILTRAR Y PRESENTAR la señal cargada
#        self.umbral = 0;
#        self.umbrales = [];
#        self.detallesSinFiltrar = [];            <-- ATRIBUTOS QUE NO FUNCIONARON
#        self.detallesFiltrados = [];
        
    def asignarControlador(self,controlador):                                               # Se asigna el controlador al modelo
        self.__controlador = controlador;
      
#%%        
    def almacenarArchivo(self,archivoCargado,nombre,tamanoEncabezado,canales):
        
        if archivoCargado.endswith(".mat"):                                                 # Ejecuta esta seccion si el archivo cargado es .mat
            diccionarioArchivo = sio.loadmat(archivoCargado);                               # Almacena el archivo cargado y muestra su "diccionario"
            print("Las claves cargadas fueron: " + str(diccionarioArchivo.keys()));
            
            if (nombre in diccionarioArchivo) == True:
                #senal = diccionarioArchivo[nombre];
                senal = np.squeeze(diccionarioArchivo[nombre]);
                
                self.redimensionarSenal(senal);
            
        
        elif archivoCargado.endswith(".txt"):
            lineas = reader_csv(open(archivoCargado,"r"));                  

            numero_fila = 0                                                                 
            encabezado = '';
            #canales = 11;
            #tamanoEncabezado = 6;
            
            senal=[];                                                                       
            
            for fila in lineas:
                if numero_fila < tamanoEncabezado:                                          # Se Imprimira el encabezado mientras la variable
                    encabezado = encabezado + fila[0] + '\n';                               # numero_fila sea menor que el tamaño del encabezado
                    numero_fila = numero_fila + 1;
                    
                else:                                                                       # En caso de haber leido el encabezado por completo
                    temporal = [];                                                          # se almacenaran los datos numéricos de cada columna          
                    contador = 0;                                                           # en el vector temporal
                    for columna in fila:
                        if contador == 0:                                                  
                            contador = contador + 1;
                            continue;
                        elif contador == canales +1:                                        
                            break;
                        else:
                            temporal.append(float(columna));                                
                                                                                            
                        contador = contador + 1;
                         
                    senal.append(temporal);                                                      
                   
            senal = np.asarray(senal,order = 'C');                                          
            senal = np.transpose(senal);                                                    # Se almacena la señal en el atributo self.senal
            self.redimensionarSenal(senal);                                                 # (Dimension = 2) y se transfiere al metodo analizar
            
#%%            
    def redimensionarSenal(self,senal):                                                     # Genera senalContinua en funcion de la dimension
        if senal.ndim == 1:                
            self.x_max = len(senal);                                                        # ndim = 1 : Solo genera su vector de tiempo
            self.senal = senal;                                                             # la señal esta en la forma señal[muestras] 
            self.banderaDimension = 1;    
            self.__controlador.graficarSenal(self.senal);                        
                          
                                                                         
        elif senal.ndim == 2:                                                               # ndim = 2: Solo genera su vector de tiempo, la
            self.x_max = senal.shape[1];                                                    # señal ya esta de la forma señal[canales,muestras]
            self.senal = senal; 
            self.banderaDimension = 2;
            self.__controlador.graficarSenal(self.senal);                       
            
            
        elif senal.ndim == 3:                                                               # ndim = 3: Genera un vector de tiempo y                                                                                   
            canales = senal.shape[0];                                                       # una señal continua de 2 dimensiones
            muestras =senal.shape[1];                                                       # señal[canales,muestras]
            epocas = senal.shape[2];                                              
            self.x_max = muestras*epocas;                        
            self.senal = np.reshape(senal,(canales,muestras*epocas),order = 'F');
            
            self.banderaDimension = 2;
            self.__controlador.graficarSenal(self.senal);  
            
#%%           
    def mostrarCanal(self,canal):                                                           # Metodo habilitado solo para señales multicanal
        if self.banderaDimension == 2:
            self.canalActual = canal;                                                        
            self.__controlador.graficarSenal(self.senal[self.canalActual,self.x_min:self.x_max]);

#%%        
    def mostrarCanales(self):                                                               # Se muestran todos los canales filtrados 
        self.canalActual = -1;                                                              # y el canal actual pasa a ser (-1)
        self.__controlador.graficarSenal(self.senal[:,self.x_min:self.x_max]);

#%%        
    def establecerRango(self,x_min,x_max,banderaRango):                                     # banderaRango determina si el usuario desea              
        self.x_min = x_min;
        self.x_max = x_max;
        
        if self.banderaDimension == 1:                                                      # establecer un rango : banderaRango == 0                  
            if banderaRango == 1:                                                           # ver la señal completa : banderaRango == 1
                self.x_min = 0;
                self.x_max = len(self.senal);
                self.__controlador.graficarSenal(self.senal[self.x_min:self.x_max]);
                
            else:
                if self.x_max <= len(self.senal):                                           # Si el usuario seleccionó un rango de tiempo                           
                    self.__controlador.graficarSenal(self.senal[self.x_min:self.x_max]);    # envia segmentada para ser graficada
            
        elif self.banderaDimension == 2:
            if banderaRango == 1:
                self.x_min = 0;
                self.x_max = self.senal.shape[1];                                           # x_max = cantidad de muestras de la señal
                
            if self.x_max <= self.senal.shape[1]:                                           # Si la señal es multicanal, se analiza si el usuario
                if self.canalActual == -1:                                                  # esta viendo 1 solo canal, o todos, con la bandera
                    self.mostrarCanales();
                
                else:
                    self.mostrarCanal(self.canalActual);
 
#%%        
    def limpiarMemoria(self):                                                               # Se reinicia la memoria del sistema
        self.senal = np.asarray([]);                                                        
        self.canalActual = 0;
        self.banderaDimension = 0;
        self.x_min = 0;
        self.x_max = 0;
        
#        self.SenalDescompuesta = np.asarray([]);                                           # Se inicializan los atributos necesarios para 
#        self.Nivel_max = 0;                                                                # FILTRAR Y PRESENTAR la señal cargada
#        self.Umbral = 0;                               NO FUNCIONARON: NO SE MODIFICABAN 
#        self.Umbrales = [];                            LAS LISTAS
#        self.DetallesSinFiltrar = [];
#        self.DetallesFiltrados = [];

#%%
    def guardarSenal(self,nombreGuardar):                                                   # Guarda la señal filtrada en un .mat con el nombre
        sio.savemat('senal filtrada.mat', {nombreGuardar : self.senalFiltrada});            # ingresado por el usuario

#%%                                                              1) RUTINA DE DESCOMPOSICION
        
    def descomponerSenal(self, nivel, umbral, ponderar, dureza):
        wavelet = [-1/np.sqrt(2) , 1/np.sqrt(2)];                                           # Filtro pasa altas
        escala = [1/np.sqrt(2) , 1/np.sqrt(2)];                                             # Filtro pasa bajas
        
        if self.banderaDimension == 1:                                                      # Se analiza la dimension de la señal (1 o 2), para
            senal = self.senal;                                                             # determinar si debe tratarse un canal particular
            longitudOriginal = len(self.senal);
        else:
            if self.canalActual == -1:                                                      # Por defecto se selecciona el primer canal si
                self.canalActual = 0;                                                       # el usuario no ingreso ninguno o está viendo varios
                senal = self.senal[0];
                longitudOriginal = len(self.senal)
            else:                                                                           
                senal = self.senal[self.canalActual];
                longitudOriginal = len(self.senal[self.canalActual]);
        
                                                                                            # Se determina la longitud original de la señal que se
                                                                                            # requiere para la reconstrucción luego del filtrado
        
                                                                                            # La descomposicion se guardara de la siguiente forma:
        aproximaciones = [senal];                                                           # [senal, aprox 1, aprox 2, ..., aprox n]                                                  
        detalles = [];                                                                      # [detalle 1, detalle 2, ..., detalle n]
        posicion = 0;
        
        self.nivel_max = np.floor(math.log(longitudOriginal/2,2)-1);                        # Se determina el nivel máximo de descomposición, en
        if nivel > self.nivel_max:                                                          # caso de que el usuario supere dicho valor, se limita
            nivel = self.nivel_max;
        
        for i in range(nivel):
            
            senalDescomponer = aproximaciones[posicion];                                    # Se recorre el vector aproximaciones, comenzando
                                                                                            # por la señal original, y guardando aproximacion
            if len(senalDescomponer) % 2 != 0:                                              # y detalle descompuesto de cada nivel en las 
                senalDescomponer = np.append(senalDescomponer,0);                           # LISTAS (aproximaciones y detalles)
        
            aproximacion = np.convolve(senalDescomponer,escala,'full');
            aproximacion = aproximacion[1::2];
        
            detalle = np.convolve(senalDescomponer,wavelet,'full');                                  
            detalle = detalle[1::2]; 
            
            aproximaciones.append(aproximacion);
            detalles.append(detalle);
            
            posicion = posicion + 1;
        
        aproximacion_n = aproximaciones[-1].copy();                                         # Se almacena la última aproximacion descompuesta, y
        detalles = detalles[::-1];                                                          # Los detalles se reordenan descendentemente:
                                                                                            # [detalle n, ..., detalle 2, detalle 1]
       
        senalDescompuesta = aproximacion_n;                                                 # La señal descompuesta constará de la unión de la
        for detalle in detalles:                                                            # aprox del ultimo nivel (aprox n) y los detalles
            senalDescompuesta = np.append(senalDescompuesta,detalle);                       # de todos los niveles en orden descendente:
                                                                                            # (aprox n, detalle n, ..., detalle 2, detalle 1)                   
        
        self.filtrar(umbral, ponderar, dureza, aproximacion_n, detalles, longitudOriginal, senalDescompuesta);
       
#%%                                                                    2) RUTINA DE FILTRADO
        
    def filtrar(self, opcionUmbral, opcionPonderar, opcionDureza, aproximacion_n, detalles, longitudOriginal, senalDescompuesta):
        
        numMuestras = 0;                                                                        
        for detalle in detalles:                                                            # Para calcular el Umbral que determina lo que es
            numMuestras = numMuestras + len(detalle);                                       # ruido, se suman laslongitud de los detalles de 
        numMuestras = numMuestras + len(aproximacion_n);                                    # cada nivel y la aproximacion del ultimo nivel
     
                                         #%% a) Análisis de la opción de umbral seleccionada  
        
        if opcionUmbral == 'Universal':       
            umbral = np.sqrt(2*(np.log(numMuestras)));                                      # Se aplica una fórmula para el umbral según la
                                                                                            # selección del usuario
        if opcionUmbral == 'Minimax':       
            umbral = 0.3936 + 0.1829*(np.log(numMuestras)/np.log(2));
            
        '''
        elif opcionUmbral == 'Sure':
            sx2 = sort(abs(x)).^2;
            risks = (n-(2*(1:n))+(cumsum(sx2)+(n-1:-1:0).*sx2))/n;
            best = min(risks);
            thr = sqrt(sx2(best));
            print('Escogio Sure \nUmbral = ', str(umbral));
        '''   
        
                                    #%% b) Análisis de la opción de ponderación seleccionada     
        banderaMultiNivel = 0;
        if opcionPonderar == 'Común':                                                       # El umbral calculado en a) no debe aplicarse,                           
            umbral = umbral;                                                                # directamente, debe ponderarse en función de  
            umbrales = [];                                                                  # diferentes criterios estadísticos, y puede 
                                                                                            # determinarse con: ninguno, el último, o todos
        if opcionPonderar == 'Primer nivel':                                                # los detalles descompuestos de la señal
            umbral = umbral*(np.median(np.absolute(detalles[-1])))/0.6745;
            umbrales = [];                                                                  # Para la opción primer nivel, el umbral se determina
                                                                                            # con el detalle del ultimo nivel descompuesto
        if opcionPonderar == 'Multi nivel':      
            banderaMultiNivel = 1;                                                          # Se activa una bandera requerida para aplicar el filtro
            umbrales = [];
            for detalle in detalles:                                                        # Para la opción multi nivel, se calcula un umbral
                sigma = (np.median(np.absolute(detalle)))/0.6745;                           # para cada detalle, y se van guardando en la                        
                umbrales.append(umbral*sigma);                                              # LISTA umbrales
                                                                                     
            
                               #%% c) Análisis de la opción de opción de dureza seleccionada         

        umbralDetalle = 0;                                                                  # Posicion empleada para recorrer 
                                                                                            # vector de umbrales en caso de existir 
                                                                                            
        if opcionDureza == 'Duro':                                                          # MECANISMO DE FILTRADO:
            if banderaMultiNivel == 1:                                                      
                for detalle in detalles:                                                    # Para filtrar una señal, debe aplicarse una ecuación
                    detalle[np.absolute(detalle) < umbrales[umbralDetalle]] = 0;            # a los detalles descompuestos, tal que cada valor
                    umbralDetalle = umbralDetalle + 1;                                      # se elimine si: 
            else:                                                                           # Su valor absoluto esta por debajo del umbral determinado.
                for detalle in detalles:                                                    
                    detalle[np.absolute(detalle) < umbral] = 0;
                                                                                            # Sí el valor absoluto del detalle está por encima del 
                                                                                            # umbral determinado, hay 2 opciones:                                                                             
            self.reconstruir(aproximacion_n, detalles, longitudOriginal, senalDescompuesta, umbral, umbrales);                        
                                                                                            # Opcion DURO: El detalle se deja intacto/igual
        if opcionDureza == 'Suave':
            detallesFiltrados = [];                                                         # Opcion SUAVE: Al valor absoluto se le resta el umbral
                                                                                            # y se multiplica por el signo del detalle
            if banderaMultiNivel == 0:                                                      # --------------------------------------------------------    
                for detalle in detalles:
                    signo = detalle.copy();                                                 # Si la opción escogida es Suave, se realiza el mismo
                    signo[signo < 0] = -1;                                                  # proceso para aplicar la formula antes descrita,
                    signo[signo >= 0] = 1;                                                  # la diferencia está en la banderaMultinivel, ya que
                                                                                            # es 1 si se escogió esta opción, y se debe emplear 
                    detalle[np.absolute(detalle) < umbral] = 0;                             # la LISTA DE UMBRALES generada.
                                                                                            # En caso de que la bandera sea 0, se aplica el mismo
                    detalleTemporal = [];                                                   # umbral a todos los detalles
                    
                    for detalle_k in range(len(detalle)):
                        if np.absolute(detalle[detalle_k]) >= umbral:
                            detalle[detalle_k] = signo[detalle_k]*(np.absolute(detalle[detalle_k])-umbral);
                        detalleTemporal.append(detalle[detalle_k]);
                    detallesFiltrados.append(detalleTemporal);
                
                
            if banderaMultiNivel == 1:                                                          
                 
                for detalle in detalles:
                    signo = detalle.copy();
                    signo[signo < 0] = -1;
                    signo[signo >= 0] = 1;
                    
                    detalle[np.absolute(detalle) < umbral] = 0;
                     
                    detalleTemporal = [];
                    
                    for detalle_k in range(len(detalle)):
                        if np.absolute(detalle[detalle_k]) >= umbral:
                            detalle[detalle_k] = signo[detalle_k]*(np.absolute(detalle[detalle_k])-umbrales[umbralDetalle]);
                        detalleTemporal.append(detalle[detalle_k]);
                    detallesFiltrados.append(detalleTemporal);
                    umbralDetalle = umbralDetalle + 1;                                          
            
            self.reconstruir(aproximacion_n, detalles, longitudOriginal, senalDescompuesta, umbral, umbrales); 

#%%                                                              3) RUTINA DE RECONSTRUCCION
            
    def reconstruir(self, aproximacion_n,detalles,longitudOriginal, senalDescompuesta, umbral, umbrales):     # Recibe la aproximacion del ultimo nivel, y los 
        detallesFiltrados = detalles;                                                       # detalles de cada nivel en orden descendente:
        wavelet_inv = [1/np.sqrt(2) , -1/np.sqrt(2)];                                       # [aprox n], [detalle n, ..., detalle 2, detalle 1]]
        escala_inv = [1/np.sqrt(2) , 1/np.sqrt(2)];
        
        niveles = [];
        
        for i in range(len(detalles)):                                      
            if i == 0:
                numPuntos = len(aproximacion_n);                                            # El mecanismo de reconstrucción es inverso al 
                                                                                            # de descomposición:
                Aproximacion = np.zeros((2*numPuntos));                                     # 1) Generando un vector de zeros de tamaño doble
                Aproximacion[0::2] = aproximacion_n;                                        # 2) Cada 2 muestras a partir de la 2, se 
                Aproximacion[1::2] = 0;                                                     # introduce la ultima aproximacion
                
                Aproximacion = np.convolve(Aproximacion,escala_inv,'full');                 # El mismo proceso a la aprox y al detalle
                                                                                            # 3) Luego se hace la convolucion con la señal inversa
                numPuntos = len(detalles[i])
                Detalle = np.zeros((2*numPuntos));
                Detalle[0::2] = detalles[i];
                Detalle[1::2] = 0;
                
                Detalle = np.convolve(Detalle,wavelet_inv,'full');                                        
                
                nivel = Aproximacion + Detalle;                                             # NOTA:
                niveles.append(nivel);                                                      # El primer "if" reconstruye sobre la aproximacion y los
                                                                                            # detalles del último nivel (con la bandera "i = 0"). 
            else:                                                                           # Una vez reconstruida, se procede en el "else" a reconstruir
                                                                                            # sobre con los residuos sucesivos.
                if len(niveles[i-1]) > len(detalles[i]):
                    nivelTemporal = niveles[i-1];                                           
                    nivelTemporal = nivelTemporal[0:len(detalles[i])];
                    niveles[i-1] = nivelTemporal;                                           # Cada residuo se almacena en la LISTA niveles
                    
                numPuntos = len(niveles[i-1]);
                Aproximacion = np.zeros((2*numPuntos));                                        
                Aproximacion[0::2] = niveles[i-1];                                            
                Aproximacion[1::2] = 0;                                                         
                
                Aproximacion = np.convolve(Aproximacion,escala_inv,'full');                 
                                                                                             
                numPuntos = len(detalles[i])
                Detalle = np.zeros((2*numPuntos));
                Detalle[0::2] = detalles[i];
                Detalle[1::2] = 0;
                
                Detalle = np.convolve(Detalle,wavelet_inv,'full');                                        
                
                nivel = Aproximacion + Detalle; 
                niveles.append(nivel);
            
            
        senalFiltrada = niveles[-1].copy();                                                 # El ultimo residuo/término representa el primer nivel, 
        senalFiltrada = senalFiltrada[0:longitudOriginal];                                  # o nivel inicial de la señal original, pero filtrado
        print(type(senalFiltrada));
        self.senalFiltrada = senalFiltrada;
        
        if self.banderaDimension == 1:
            self.__controlador.graficarSenales(self.senal[self.x_min:self.x_max],
                                           senalFiltrada[self.x_min:self.x_max],
                                           senalDescompuesta,
                                           detallesFiltrados,
                                           umbral,
                                           umbrales,
                                           self.nivel_max); 
        
        if self.banderaDimension == 2: 
            self.__controlador.graficarSenales(self.senal[self.canalActual,self.x_min:self.x_max],
                                           senalFiltrada[self.x_min:self.x_max],
                                           senalDescompuesta,
                                           detallesFiltrados,
                                           umbral,
                                           umbrales,
                                           self.nivel_max);  
                                               
                                                                                               
#%%        
        
        
        
        