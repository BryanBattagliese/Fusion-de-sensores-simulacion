# """ """ """ """ """ """ """ """ """ """ """ """ #                                              
# GIAR                                            #  
# Fusion de sensores en ambiente estructurado     #                                           
# Bryan A. Battagliese Montiel                    #                          
# 2024                                            #  
#                                                 #  
# """ """ """ """ """ """ """ """ """ """ """ """ #   
import sim
import simConst
import time
import math
import numpy as np
import json
import os

# en el coppeliaSim debe estar en un script simRemoteApi.start(19997,1000,true,true)

#========================================================
#                       Constantes
VEL_BUSQUEDALINEA = 2         # Velocidad baja 1.5
VEL_AVANCE = 2
VEL_GIRO_DIRECCION = 0.2      # Es la velocidad con que gira
GRADOS_INCERTIDUMBRE = 1      # 1.5º
GRADOS_INCERDIDUMBRE_CONSULTA = 5
POS_INCERTIDUMBRE = 0.005     # 0,5 cm
LONG_CELDA = 0.4              # La longitud de la celda es de 40cm
POSICIONES = []
DELTA = 3
#========================================================
#                      Variables globales
clientID = 0      # Handle del entorno CoppeliaSim
H_floor = 0       # Handle del piso 
                  # Manejadores del robot
H_rueda_Izq = 0
H_rueda_Der = 0
H_uS_adelante = 0
H_uS_atras = 0 
H_uS_der = 0
H_uS_izq = 0
H_minipi = 0
H_linea_izq = 0
H_linea_C_izq = 0
H_linea_der = 0 
H_linea_C_der = 0

mapeo = 'data/mapeador.txt'
ultimo_mapa = 'data/ultimo_mapa.txt'
mapa_anterior = 'data/mapa_anterior.txt'
binario = 'data/binario.txt'

#========================================================
#                       Funciones

#========================================================
# Función: extraer_dato (posición) 
# Descripción: extrae el valor de una determonada posición
#               de un vector(dataFrame)
# Devuelve: el valor numérico
#========================================================
def extraer_dato(posicion,vector):
    dato1temp=vector[0]
    dato2temp=dato1temp[posicion]
    return dato2temp

#========================================================
# Función: linea () 
# Descripción: posee una variable umbral, si el valor 
#               es major que ese umbral supone que detectó 
#               la línea
# Devuelve: 1 si sensa la línea en blanco
#           0 si no la sensa
#========================================================
def linea ():
    data_umbral=0.35
    #print ('Leo sensores e visión')
    res,dato,dato2=sim.simxReadVisionSensor(clientID,H_linea_izq,sim.simx_opmode_blocking)
    dat_temp=extraer_dato(0,dato2)
    if dat_temp>=data_umbral: data_linea_izq=1 
    else: data_linea_izq=0

    res,data1,dato2=sim.simxReadVisionSensor(clientID,H_linea_C_izq,sim.simx_opmode_blocking)
    dat_temp=extraer_dato(0,dato2)
    if dat_temp>=data_umbral: data_linea_C_izq=1 
    else: data_linea_C_izq=0

    res,data1,dato2=sim.simxReadVisionSensor(clientID,H_linea_der,sim.simx_opmode_blocking)
    dat_temp=extraer_dato(0,dato2)
    if dat_temp>=data_umbral: data_linea_der=1 
    else: data_linea_der=0 
    
    res,data1,dato2=sim.simxReadVisionSensor(clientID,H_linea_C_der,sim.simx_opmode_blocking)
    dat_temp=extraer_dato(0,dato2)
    if dat_temp>=data_umbral: data_linea_C_der=1 
    else: data_linea_C_der=0  

    return data_linea_izq,data_linea_C_izq,data_linea_C_der,data_linea_der

#========================================================
# Función: estado (delta) 
# Descripción: El valor de delta es la incertidumbre
#    que se admite cerca del ángulo buscado.
#    Típicamente 3º
# Devuelve: Estado=0 -- si está cerca del 0°
#           Estado=1 -- si está cerca del 90°
#           Estado=2 -- si está cerca del 180°
#           Estado=3 -- si está cerca del 270°
#           Estado=5 -- No puede saber
#========================================================
def estado (delta):
    res,eulerAngles=sim.simxGetObjectOrientation(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
    gama=eulerAngles[2]*180/math.pi
    if (((gama>=-delta)and (gama<=0)) or ((gama>=0)and (gama<=delta))): # X+
        #print ('Legué al Estado 0,el ángulo es:', gama)
        return 0
    if ((gama>360-delta) and (gama<=360)):                  # X+
        #print ('Legué al Estado 0,el ángulo es:', gama)
        return 0    
    if (gama<=90+delta) and (gama>=90-delta):               # Y+
       #print ('Legué al Estado 1, el ángulo es:', gama)
       return 1
    if (gama<=-270+delta) and (gama>=-270-delta):           # Y+
       #print ('Legué al Estado 1, el ángulo es:', gama)
       return 1
    if (gama<=180+delta) and (gama>=180-delta):             # X-
       #print ('Legué al Estado 2, el ángulo es:', gama)
        return 2
    if (gama<=-180+delta) and (gama>=-180-delta):           # X-
        #print ('Legué al Estado 2, el ángulo es:', gama)
        return 2
    if (gama<=270+delta) and (gama>=270-delta):             # Y-
        #print ('Legué al Estado 3, el ángulo es:', gama)
        return 3
    if (gama<=-90+delta) and (gama>=-90-delta):             # Y-
        #print ('Legué al Estado 3, el ángulo es:', gama)
        return 3	

#========================================================
# Función: get_orientacion(delta) 
# Descripción: El valor de delta es la incertidumbre
#    que se admite cerca del ángulo buscado.
#    Típicamente 3º
# Devuelve: X+ -- si está X+
#           X- -- si está X-
#           Y+ -- si está Y+
#           Y- -- si está Y-
#           0 --- si no pudo detectar el sentido
#========================================================
def get_orientacion (delta):
    res,eulerAngles=sim.simxGetObjectOrientation(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
    gama=eulerAngles[2]*180/math.pi
    if (((gama>=-delta)and (gama<=0)) or ((gama>=0)and (gama<=delta))): # X+
        #print ('Llegué al Estado 0,el ángulo es:', gama)
        return 'X+'
    if ((gama>360-delta) and (gama<=360)):                  # X+
        #print ('Llegué al Estado 0,el ángulo es:', gama)
        return 'X+' 
    if (gama<=90+delta) and (gama>=90-delta):               # Y+
       #print ('Llegué al Estado 1, el ángulo es:', gama)
       return 'Y+'
    if (gama<=-270+delta) and (gama>=-270-delta):           # Y+
       #print ('Llegué al Estado 1, el ángulo es:', gama)
       return 'Y+'
    if (gama<=180+delta) and (gama>=180-delta):             # X-
        #print ('Llegué al Estado 2, el ángulo es:', gama)
        return 'X-'
    if (gama<=-180+delta) and (gama>=-180-delta):           # X-
        #print ('Llegué al Estado 2, el ángulo es:', gama)
        return 'X-'
    if (gama<=270+delta) and (gama>=270-delta):             # Y-
        #print ('Llegué al Estado 3, el ángulo es:', gama)
        return 'Y-'
    if (gama<=-90+delta) and (gama>=-90-delta):             # Y-
        #print ('Llegué al Estado 3, el ángulo es:', gama)
        return 'Y-'	
    return 0

#========================================================
# Función: set_orientacion(delta) 
# Descripción: El valor de delta es la incertidumbre
#    que se admite cerca del ángulo buscado.
#    Típicamente 3º
# Devuelve: 1 --- si pudo setear el sentido
#           0 --- si no pudo setear el sentido
#========================================================
def set_orientacion (data):
    if data=='X+':
        girar_x_positivo ()
        return 1
    if data=='X-':
        girar_x_negativo ()
        return 1   
    if data=='Y+':
        girar_y_positivo ()
        return 1
    if data=='Y-':
        girar_y_negativo ()
        return 1 
    return 0

#========================================================
# Función: parar () 
#
# Devuelve: No devuelve nada
#========================================================
def parar ():
    print ('Paró')
    velocidad=0.0
    sim.simxSetJointTargetVelocity(clientID,H_rueda_Izq,velocidad,sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID,H_rueda_Der,velocidad,sim.simx_opmode_streaming)
    return 0

#========================================================
# Función: obstaculo ()
# Descripción: detecta un obstáculo 
# Devuelve: 0 si NO dectectó un obstáculo
#           1 si dectectó un obstáculo
#========================================================
def obstaculo (ultrasonido):
    res,distance,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,ultrasonido,sim.simx_opmode_streaming)
    if (distance==True):
        return 1
    return 0 

#========================================================
# Función: detectar_pared (ultrasonido)
# Descripción: detecta una pared.
# Devuelve: True si la hay.
#           False si no la detecta.
#========================================================
def detectar_pared (ultrasonido):
    res,distance,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,ultrasonido,sim.simx_opmode_blocking)
    return distance 

#========================================================
# Función: distancia (ultrasonido)
# Descripción: mide la distancia de un ultrasonido 
#              específico
# Devuelve: distancia en metros
#========================================================
def distancia (ultrasonido):
    res,distance,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,ultrasonido,sim.simx_opmode_blocking)
    if(distance==True):
        distance=math. sqrt(math.pow(detectedPoint[0],2)+math.pow(detectedPoint[1],2)+math.pow(detectedPoint[2],2)) 
    else:
        distance=0
    return distance

#==========================================================
# Función: avanzar_pared (velocidad)
# Descripción: Avanza derecho a una velocidad hasta chocarse
#   con una pared
# Devuelve: 0
#==========================================================
def avanzar_pared (velocidad):
    #print ('Avanza')
    sim.simxSetJointTargetVelocity(clientID,H_rueda_Izq,velocidad,sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID,H_rueda_Der,velocidad,sim.simx_opmode_streaming)
    detectar_pared ()
    return 0

#==========================================================
# Función: vel_mot(motor,velocidad)
# Descripción: Setea la velocidad en un motor
# Devuelve: 
#==========================================================
def vel_mot(motor,velocidad):
     sim.simxSetJointTargetVelocity(clientID,motor,velocidad,sim.simx_opmode_oneshot)
     return 0

#==========================================================
# Función: avanzar(velocidad)
# Descripción: Avanza derecho a una velocidad
# Devuelve: 
#==========================================================
def avanzar (velocidad):
    #print ('Avanza')
    vel_mot(H_rueda_Izq,velocidad)
    vel_mot(H_rueda_Der,velocidad)
    return 0

#==========================================================
# Función: avanzar_linea(velocidad)
# Descripción: Avanza derecho y cuando sensa una línea 
#              mueve las ruedas y se pone derecho
# Devuelve: 0- si hubo un error
#           1- si sensó la línea y se pudo poner derecho
#==========================================================
def avanzar_linea (velocidad):
    #print ('Avanza y busqueda de línea')
    # Avanza si no hay obstáculos en esa dirección
    avanzar (velocidad)
    # Busco la línea
    s_izq,sc_izq,sc_der,s_der=linea ()
    #print('El valor de los sensores de linea es', s_izq,sc_izq,sc_der,s_der)
    #sim.simxAddStatusbarMessage(clientID,'El valor de los sensores de linea es :'+str(s_izq)+" "+str(sc_izq)+" "+str(sc_der)+" "+str(s_der),sim.simx_opmode_oneshot)
    #muestra=0
    # Busca que un sensor se active
    while (s_izq==0 and sc_izq==0 and sc_der==0 and s_der==0):
             s_izq,sc_izq,sc_der,s_der=linea ()
             #print('Muestra:'+str(muestra)+'-'+'El valor de los sensores de linea es', s_izq,sc_izq,sc_der,s_der)
             #sim.simxAddStatusbarMessage(clientID,'Muestra:'+str(muestra)+'-El valor de los sensores de linea es :'+str(s_izq)+" "+str(sc_izq)+" "+str(sc_der)+" "+str(s_der),sim.simx_opmode_oneshot)
             #muestra=muestra+1
    parar()
    # Si sensa los dos sensores del centro está ok
    if (s_izq,sc_izq,sc_der,s_der)==(0,1,1,0):
        #print ('Sensó los dos centrales')
        sim.simxAddStatusbarMessage(clientID,'Sensó los dos centrales',sim.simx_opmode_oneshot)
        return 1
    # Si sensa los dos sensores del extremo está ok
    if (s_izq,sc_izq,sc_der,s_der)==(1,0,0,1):
        #print ('Sensó los dos extremos')
        sim.simxAddStatusbarMessage(clientID,'Sensó los dos extremos',sim.simx_opmode_oneshot)
        return 1
    # Si sensa el sensor izquierdo central avanza con el motor derecho
    # hasta sensar el sensor derecho central
    if (s_izq,sc_izq,sc_der,s_der)==(0,1,0,0):
        #print ('Sensó el sensor izquierdo central')
        sim.simxAddStatusbarMessage(clientID,'Sensó el sensor izquierdo central',sim.simx_opmode_oneshot)
        #vel_mot(H_rueda_Der,velocidad)
        #s_izq,sc_izq,sc_der,s_der=linea ()
        #while sc_der==0:
        #    s_izq,sc_izq,sc_der,s_der=linea ()
        #parar()
        return 1
    # Si sensa el sensor derecho central avanza con el motor izquierdo
    # hasta sensar el sensor izquierdo central
    if (s_izq,sc_izq,sc_der,s_der)==(0,0,1,0):
        #print ('Sensó el sensor derecho central')
        sim.simxAddStatusbarMessage(clientID,'Sensó el sensor derecho central',sim.simx_opmode_oneshot)
        #vel_mot(H_rueda_Izq,velocidad)
        #s_izq,sc_izq,sc_der,s_der=linea ()
        #while sc_izq==0:
        #    s_izq,sc_izq,sc_der,s_der=linea ()
        #parar()
        return 1
    # Si sensa el sensor izquierdo externo avanza con el motor derecho
    # hasta sensar el sensor derecho externo
    if (s_izq,sc_izq,sc_der,s_der)==(1,0,0,0) or (s_izq,sc_izq,sc_der,s_der)==(1,1,0,0):
        #print ('Sensó el sensor izquierdo externo')
        sim.simxAddStatusbarMessage(clientID,'Sensó el sensor izquierdo externo',sim.simx_opmode_oneshot)
        #vel_mot(H_rueda_Der,velocidad)
        #s_izq,sc_izq,sc_der,s_der=linea ()
        #while s_der==0:
        #    s_izq,sc_izq,sc_der,s_der=linea ()
        #parar()
        return 1
    # Si sensa el sensor derecho externo avanza con el motor izquierdo
    # hasta sensar el sensor izquierdo externo
    if (s_izq,sc_izq,sc_der,s_der)==(0,0,0,1) or (s_izq,sc_izq,sc_der,s_der)==(0,0,1,1):
        #print ('Sensó el sensor derecho externo')
        sim.simxAddStatusbarMessage(clientID,'Sensó el sensor derecho externo',sim.simx_opmode_oneshot)
        #vel_mot(H_rueda_Izq,velocidad)
        #s_izq,sc_izq,sc_der,s_der=linea ()
        #while s_izq==0:
        #    s_izq,sc_izq,sc_der,s_der=linea ()
        #parar()
        return 1
    return 0

#==========================================================
# Función: avanzar_1_celda(velocidad)
# Descripción: Avanza derecho la distancia de 1 celda
#              a una velocidad determinada. En el robot
#              real se haría con el encoder de cuadratura.
# Devuelve: 0- Si hay un obstáculo (pared) en el sentido de
#              avance
#           1- Si todo está OK
#           2- Si no pudo detectar el sentido a donde apunta
#              el robot.
#==========================================================
def avanzar_1_celda (velocidad):
    
    nombre_instruccion = "avanzar"
    print ('El minipi avanza una celda')
    # pregunto en dónde estoy apuntando
    sentido=get_orientacion(GRADOS_INCERDIDUMBRE_CONSULTA)
    if sentido=='X+':
        res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        x=x1
        x1=x1+LONG_CELDA
        avanzar (velocidad)
        while abs(x-x1)>POS_INCERTIDUMBRE:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        parar()
        return 1
    if sentido=='X-':
        res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        x=x1
        x1=x1-LONG_CELDA
        avanzar (velocidad)
        while abs(x-x1)>POS_INCERTIDUMBRE:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        parar()
        return 1
    if sentido=='Y+':
        res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        y=y1
        y1=y1+LONG_CELDA
        avanzar (velocidad)
        while abs(y-y1)>POS_INCERTIDUMBRE:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        parar()       
        return 1
    if sentido=='Y-':
        res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        y=y1
        y1=y1-LONG_CELDA
        avanzar (velocidad)
        while abs(y-y1)>POS_INCERTIDUMBRE:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        parar()        
        return 1
    return 3

    mapear()

#========================================================
# Función: girar_izq ()
# Descripción: Usa la orientación del cuerpo del MiniPi
#   para rotar. La velocidad de roración tiene que ser baja
# Devuelve: 
#========================================================
def girar_izq ():
    
    nombre_instruccion = "girar"
    
    print ('Girar Izquierda')
    delta_busqueda=GRADOS_INCERTIDUMBRE
    estado_inic=estado(10)
    estado_final=5          # Se pone un valor >< de 0 a 3
    vel_mot(H_rueda_Izq,-VEL_GIRO_DIRECCION)
    vel_mot(H_rueda_Der,VEL_GIRO_DIRECCION)
    #print('Estado inicial :', estado_inic)
    if estado_inic==0:
        #print ('Estoy preguntando por si llego al ESTADO 1 ')
        while estado_final !=1:
              estado_final=estado(delta_busqueda)
    elif estado_inic==1:
        #print ('Estoy preguntando por si llego al ESTADO 2 ')
        while estado_final !=2:
            estado_final=estado(delta_busqueda)
    elif estado_inic==2:
        #print ('Estoy preguntando por si llego al ESTADO 3 ')
        while estado_final !=3:
            estado_final=estado(delta_busqueda)
    elif estado_inic==3:
       # print ('Estoy preguntando por si llego al ESTADO 0 ')
        while estado_final !=0:
            estado_final=estado(delta_busqueda)
    #print('Llegué al estafo final ', estado_final)
    parar()
    
    #mapear()

#========================================================
# Función: girar_der ()
# Descripción: Usa la orientación del cuerpo del MiniPi
#   para rotar. La velocidad de roración tiene que ser baja
# Devuelve:
#========================================================
def girar_der ():
    
    nombre_instruccion = "girar"
    
    print ('Girar Derecha')
    delta_busqueda=GRADOS_INCERTIDUMBRE
    estado_inic=estado(10)
    estado_final=4          # Se pone un valor >< de 0 a 3
    vel_mot(H_rueda_Izq,VEL_GIRO_DIRECCION)
    vel_mot(H_rueda_Der,-VEL_GIRO_DIRECCION)
   #print('Estado inicial :', estado_inic)
    if estado_inic==0:
        #print ('Estoy preguntando por si llego al ESTADO 3 ')
        while estado_final !=3:
              estado_final=estado(delta_busqueda)
    elif estado_inic==1:
        #print ('Estoy preguntando por si llego al ESTADO 0 ')
        while estado_final !=0:
            estado_final=estado(delta_busqueda)
    elif estado_inic==2:
        #print ('Estoy preguntando por si llego al ESTADO 1 ')
        while estado_final !=1:
            estado_final=estado(delta_busqueda)
    elif estado_inic==3:
        #print ('Estoy preguntando por si llego al ESTADO 2 ')
        while estado_final !=2:
            estado_final=estado(delta_busqueda)
    #print('Llegué al estafo final ', estado_final)
    parar()
    
    #mapear()

#==========================================================
# Función: volver()
# Descripción: Lo usa la función centrar
# Devuelve: 
#==========================================================
def volver ():
        s_izq,sc_izq,sc_der,s_der=linea ()
        #print('El valor de los sensores de linea es', s_izq,sc_izq,sc_der,s_der)
        sim.simxAddStatusbarMessage(clientID,'El valor de los sensores de linea es :'+str(s_izq)+" "+str(sc_izq)+" "+str(sc_der)+" "+str(s_der),sim.simx_opmode_oneshot)        
        girar_der ()
        girar_der ()
        avanzar_pared(5)
        girar_der ()
        girar_der ()
        parar()
        return 0

#==========================================================
# Función: sensar_4uS()
# Descripción: busca cuantas paredes posee la celda
# Devuelve: 0- si no tetecta paredes
#           1- si detecta 1 pared
#           2- si detecta 2 paredes
#           3- si detecta 3 paredes
#           4- si detecta 4 paredes
#==========================================================
def sensar_4uS():
    paredes=0
    if detectar_pared (H_uS_adelante)==True:
        paredes=paredes+1
    if detectar_pared (H_uS_atras)==True:
        paredes=paredes+1    
    if detectar_pared (H_uS_der)==True:
        paredes=paredes+1    
    if detectar_pared (H_uS_izq)==True:
        paredes=paredes+1        
    return paredes

#==========================================================
# Función: get_distancia_4uS()
# Descripción: Mide la distancia de los ultrasonidos
# Devuelve: la distancia de los ultrasonidos en el siguiente órden
#           (delantero, trasero, derecha, izquierda)
#           Si el ultrasonido no midió devuelve 0.
#           Las medidas estan en metros
#==========================================================
def get_distancia_4uS():
    dist_4uS=(distancia(H_uS_adelante),distancia(H_uS_atras),distancia(H_uS_der),distancia(H_uS_izq))
    return dist_4uS

#==========================================================
# Función: get_posicion()
# Descripción: en qué posición se encuentra el robot
# Devuelve: la posición del robot en relación con el piso
#==========================================================
def get_posicion():
 res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
 return (x1,y1,z1)

#========================================================
# Función: estoy_x_positivo (delta)
# Descripción: Pregunta si el robot esta paralelo al eje x
#              en sentido hacia el positivo.
#              Delta es un factor de incertidumbre, 
#              generalmente 3º
# Devuelve: 0- Si no es así
#           1- Si es así
#========================================================
def estoy_x_positivo (delta):
    res,eulerAngles=sim.simxGetObjectOrientation(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
    gama=eulerAngles[2]*180/math.pi
    # Pregunto si estoy a 90º, o sea // al eje Y+
    if (((gama<=delta)and (gama>=0)) or (gama>=360-delta)):
       return 1
    else:
        return 0

#========================================================
# Función: girar_x_positivo ()
# Descripción: Usa la orientación del cuerpo del MiniPi
#   para rotar. La velocidad de rotación tiene que ser baja
# Devuelve: 0
#========================================================
def girar_x_positivo ():
    #print ('Posiciona el robot en X+')
    if estoy_x_positivo (GRADOS_INCERTIDUMBRE):
        #print ('El Robot está en X+')
        print('\n')
    else:
        if get_orientacion (GRADOS_INCERDIDUMBRE_CONSULTA)=='Y-':
            vel_mot(H_rueda_Izq,-VEL_GIRO_DIRECCION)
            vel_mot(H_rueda_Der,VEL_GIRO_DIRECCION)
        else:
            vel_mot(H_rueda_Izq,VEL_GIRO_DIRECCION)
            vel_mot(H_rueda_Der,-VEL_GIRO_DIRECCION)
        while estoy_x_positivo (GRADOS_INCERTIDUMBRE)==0:
            # No hace nada
            dummy=0
        #print ('El Robot está en X+')
        parar()
    return 0

#========================================================
# Función: estoy_x_negativo (delta)
# Descripción: Pregunta si el robot esta paralelo al eje x
#              en sentido hacia el negativo.
#              Delta es un factor de incertidumbre, 
#              generalmente 3º
# Devuelve: 0- Si no es así
#           1- Si es así
#========================================================
def estoy_x_negativo (delta):
    res,eulerAngles=sim.simxGetObjectOrientation(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
    gama=eulerAngles[2]*180/math.pi
    # Pregunto si estoy a 90º, o sea // al eje Y+
    if ((gama<=180+delta) and (gama>=180-delta))or((gama<=-180+delta) and (gama>=-180-delta)):
       return 1
    else:
        return 0

#========================================================
# Función: girar_x_negativo ()
# Descripción: Usa la orientación del cuerpo del MiniPi
#   para rotar. La velocidad de rotación tiene que ser baja
# Devuelve: 0
#========================================================
def girar_x_negativo ():
    #print ('Posiciona el robot en X-')
    if estoy_x_negativo (GRADOS_INCERTIDUMBRE):
        print('\n')
        #print ('El Robot está en X-')
    else:
        if get_orientacion (GRADOS_INCERDIDUMBRE_CONSULTA)=='Y+':
            vel_mot(H_rueda_Izq,-VEL_GIRO_DIRECCION)
            vel_mot(H_rueda_Der,VEL_GIRO_DIRECCION)
        else:
            vel_mot(H_rueda_Izq,VEL_GIRO_DIRECCION)
            vel_mot(H_rueda_Der,-VEL_GIRO_DIRECCION)
        while estoy_x_negativo (GRADOS_INCERTIDUMBRE)==0:
            # No hace nada
            dummy=0
        #print ('El Robot está en X-')
        parar()
    return 0

#========================================================
# Función: estoy_y_positivo (delta)
# Descripción: Pregunta si el robot esta paralelo al eje y
#              en sentido hacia el positivo.
#              Delta es un factor de incertidumbre, 
#              generalmente 3º
# Devuelve: 0- Si no es así
#           1- Si es así
#========================================================
def estoy_y_positivo (delta):
    res,eulerAngles=sim.simxGetObjectOrientation(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
    gama=eulerAngles[2]*180/math.pi
    # Pregunto si estoy a 90º, o sea // al eje Y+
    if ((gama<=90+delta) and (gama>=90-delta))or((gama<=-270+delta) and (gama>=-270-delta)):
       return 1
    else:
        return 0

#========================================================
# Función: girar_y_positivo ()
# Descripción: Usa la orientación del cuerpo del MiniPi
#   para rotar. La velocidad de roración tiene que ser baja
# Devuelve: 0
#========================================================
def girar_y_positivo ():
    #print ('Posiciona el robot en Y+')
    if estoy_y_positivo (GRADOS_INCERTIDUMBRE):
        #print ('El Robot está en Y+')
        print('\n')
    else:
        if get_orientacion (GRADOS_INCERDIDUMBRE_CONSULTA)=='X+':
            vel_mot(H_rueda_Izq,-VEL_GIRO_DIRECCION)
            vel_mot(H_rueda_Der,VEL_GIRO_DIRECCION)
        else:
            vel_mot(H_rueda_Izq,VEL_GIRO_DIRECCION)
            vel_mot(H_rueda_Der,-VEL_GIRO_DIRECCION)
        while estoy_y_positivo (GRADOS_INCERTIDUMBRE)==0:
            # No hace nada
            dummy=0
        #print ('El Robot está en Y+')
        parar()
    return 0

#========================================================
# Función: estoy_y_negativo (delta)
# Descripción: Pregunta si el robot esta paralelo al eje y
#              en sentido hacia el negativo.
#              Delta es un factor de incertidumbre, 
#              generalmente 3º
# Devuelve: 0- Si no es así
#           1- Si es así
#========================================================
def estoy_y_negativo (delta):
    res,eulerAngles=sim.simxGetObjectOrientation(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
    gama=eulerAngles[2]*180/math.pi
    # Pregunto si estoy a 90º, o sea // al eje Y+
    if ((gama<=270+delta) and (gama>=270-delta))or((gama<=-90+delta) and (gama>=-90-delta)):
       return 1
    else:
        return 0

#========================================================
# Función: girar_y_negativo ()
# Descripción: Usa la orientación del cuerpo del MiniPi
#   para rotar. La velocidad de roración tiene que ser baja
# Devuelve: 0
#========================================================
def girar_y_negativo ():
    #print ('Posiciona el robot en Y-')
    if estoy_y_negativo (GRADOS_INCERTIDUMBRE):
        print('\n')
        #print ('El Robot está en Y-')
    else:
        if get_orientacion (GRADOS_INCERDIDUMBRE_CONSULTA)=='X-':
            vel_mot(H_rueda_Izq,-VEL_GIRO_DIRECCION)
            vel_mot(H_rueda_Der,VEL_GIRO_DIRECCION)
        else:
            vel_mot(H_rueda_Izq,VEL_GIRO_DIRECCION)
            vel_mot(H_rueda_Der,-VEL_GIRO_DIRECCION)
        while estoy_y_negativo (GRADOS_INCERTIDUMBRE)==0:
            # No hace nada
            dummy=0
        #print ('El Robot está en Y-')
        parar()
    return 0

#==========================================================
# Función: centrar()
# Descripción: Se posiciona en el centro de una celda
# Devuelve: 0- Si detecto cero paredes
#           1- Si detectó 1 pared
#           2- Si detectó 2 paredes
#           3- Si detectó 3 paredes
#           4- Si detectó 4 paredes
#           5- Si hubo un error        
#==========================================================
def centrar ():
    
    print ('Centrando en la celda')
    vel_busquedaLínea = VEL_BUSQUEDALINEA
    incertidumbre_poscicion = POS_INCERTIDUMBRE  # Medio centímetro
    paredes=sensar_4uS()
    #print ('Cantidad de paredes= '+ str(paredes))

    if paredes==0:
        # Movimientos en Y
        girar_y_positivo ()
        avanzar_linea(vel_busquedaLínea)   
        res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        girar_y_negativo ()                 
        avanzar_linea(vel_busquedaLínea)    
        res,(x2,y2,z2)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        girar_y_positivo () 
        avanzar(vel_busquedaLínea)
        res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        while ((((y2-y1)/2)+y1)-y)>incertidumbre_poscicion:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        parar()
        # Movimientos en X 
        girar_x_positivo ()
        avanzar_linea(vel_busquedaLínea)    
        res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        girar_x_negativo ()                
        avanzar_linea(vel_busquedaLínea)    
        res,(x2,y2,z2)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        girar_x_positivo () 
        avanzar(vel_busquedaLínea)
        res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        while ((((x2-x1)/2)+x1)-x)>incertidumbre_poscicion:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
        parar()
        return 0
    
    if paredes==1:
        # En qué eje esta la pared
        girar_y_positivo ()
        # Estoy preguntando por Y+ e Y-
        if detectar_pared (H_uS_adelante)==True or detectar_pared (H_uS_atras)==True:
            # En Y+ o Y- tengo una pared, el movimiento se hace en X
            girar_x_positivo ()
            avanzar_linea(vel_busquedaLínea)    
            res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            girar_x_negativo ()                 
            avanzar_linea(vel_busquedaLínea)    
            res,(x2,y2,z2)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            girar_x_positivo () 
            avanzar(vel_busquedaLínea)
            res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            while ((((x2-x1)/2)+x1)-x)>incertidumbre_poscicion:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            parar()
            # Movimiento en Y
            girar_y_positivo ()
            if detectar_pared (H_uS_adelante)==True:
                # Si salgo por acá significa que en Y+ está la pared
                girar_y_negativo ()
                avanzar_linea(vel_busquedaLínea)
                girar_y_positivo ()
                l1=distancia(H_uS_adelante)
                l=l1
                avanzar(vel_busquedaLínea)
                while abs((l1/2)+0.01-l)>incertidumbre_poscicion:
                    l=distancia(H_uS_adelante)
                parar()
                girar_y_negativo ()
                return 1
            else:   # Si salgo por acá significa que en Y- está la pared
                avanzar_linea(vel_busquedaLínea)
                girar_y_negativo ()
                l1=distancia(H_uS_adelante)
                l=l1
                avanzar(vel_busquedaLínea)
                while abs((l1/2)+0.01-l)>incertidumbre_poscicion:
                    l=distancia(H_uS_adelante)
                parar()
                girar_y_positivo ()
                return 1   
        else:  # En X+ o X- tengo una pared, el movimiento se hace en Y
            girar_y_positivo ()
            avanzar_linea(vel_busquedaLínea)    
            res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            girar_y_negativo ()                 
            avanzar_linea(vel_busquedaLínea)    
            res,(x2,y2,z2)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            girar_y_positivo () 
            avanzar(vel_busquedaLínea)
            res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            while ((((y2-y1)/2)+y1)-y)>incertidumbre_poscicion:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            parar()
            # Movimiento en X
            girar_x_positivo ()
            if detectar_pared (H_uS_adelante)==True:
                # Si salgo por acá significa que en X+ está la pared
                girar_x_negativo ()
                time.sleep(1)
                avanzar_linea(vel_busquedaLínea)
                girar_x_positivo ()
                l1=distancia(H_uS_adelante)
                l=l1
                avanzar(vel_busquedaLínea)
                while abs((l1/2)+0.01-l)>incertidumbre_poscicion:
                    l=distancia(H_uS_adelante)
                parar()
                girar_x_negativo ()
                return 1
            else:   # Si salgo por acá significa que en X- está la pared
                time.sleep(1)
                avanzar_linea(vel_busquedaLínea)
                girar_x_negativo ()
                l1=distancia(H_uS_adelante)
                l=l1
                avanzar(vel_busquedaLínea)
                #while abs((l1/2)-0.05-l)>incertidumbre_poscicion:
                while abs((l1/2)+0.01-l)>incertidumbre_poscicion:
                    l=distancia(H_uS_adelante)
                parar()
                girar_x_positivo ()
                return 1

    if paredes==2:
        # En qué eje esta la pared
        girar_y_positivo ()
        if detectar_pared (H_uS_adelante)==True and detectar_pared (H_uS_atras)==True:
            # Hay paredes en Y opuestas
            # Me muevo en X
            girar_x_positivo ()
            time.sleep(2)
            avanzar_linea(vel_busquedaLínea)    
            res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            girar_x_negativo ()                 
            avanzar_linea(vel_busquedaLínea)    
            res,(x2,y2,z2)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            girar_x_positivo () 
            avanzar(vel_busquedaLínea)
            res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            while ((((x2-x1)/2)+x1)-x)>incertidumbre_poscicion:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            parar()
            # Me muevo en Y
            girar_y_positivo ()
            time.sleep(2) 
            l_adelante=distancia(H_uS_adelante)+0.02
            l_atras=distancia(H_uS_atras)+0.02
            diferencia_distancia=l_adelante-l_atras
            if diferencia_distancia>0:
                # Tengo que avanzar
                l=l_adelante
                avanzar(vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_adelante)
                parar()
                girar_x_positivo ()
            else:
                # Tengo que retroceder
                l=l_atras
                avanzar(-vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_atras)
                parar()
                girar_x_positivo ()
            return 2
        if detectar_pared (H_uS_der)==True and detectar_pared (H_uS_izq)==True:
            # Hay paredes en X opuestas
            # Me muevo en Y
            girar_y_positivo ()
            time.sleep(2)
            avanzar_linea(vel_busquedaLínea)    
            res,(x1,y1,z1)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            girar_y_negativo ()                 
            avanzar_linea(vel_busquedaLínea)    
            res,(x2,y2,z2)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            girar_y_positivo () 
            avanzar(vel_busquedaLínea)
            res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            while ((((y2-y1)/2)+y1)-y)>incertidumbre_poscicion:
                    res,(x,y,z)=sim.simxGetObjectPosition(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            parar()
            # Me muevo en X
            girar_x_positivo ()
            time.sleep(2) 
            l_adelante=distancia(H_uS_adelante)+0.02
            l_atras=distancia(H_uS_atras)+0.02
            diferencia_distancia=l_adelante-l_atras
            if diferencia_distancia>0:
                # Tengo que avanzar
                l=l_adelante
                avanzar(vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_adelante)
                parar()
                girar_y_positivo ()
            else:
                # Tengo que retroceder
                l=l_atras
                avanzar(-vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_atras)
                parar()
                girar_y_positivo ()
            return 2
        if detectar_pared (H_uS_adelante)==True and detectar_pared (H_uS_izq)==True:
            # Hay paredes en Y+ y X-
            # Gigo a Y-
            girar_y_negativo ()
            time.sleep(1)
            avanzar_linea(vel_busquedaLínea)
            girar_y_positivo ()
            l1=distancia(H_uS_adelante)
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            # Me muevo en el eje  X
            girar_x_positivo ()
            time.sleep(1)
            avanzar_linea(vel_busquedaLínea)
            girar_x_negativo ()
            l1=distancia(H_uS_adelante)
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            girar_y_negativo()
            return 2
        if detectar_pared (H_uS_adelante)==True and detectar_pared (H_uS_der)==True:
            # Hay paredes en Y+ y X+
            # Gigo a Y-
            girar_y_negativo ()
            time.sleep(1)
            avanzar_linea(vel_busquedaLínea)
            girar_y_positivo ()
            l1=distancia(H_uS_adelante)
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            # Me muevo en el eje  X
            girar_x_negativo ()
            time.sleep(1)
            avanzar_linea(vel_busquedaLínea)
            girar_x_positivo ()
            l1=distancia(H_uS_adelante)
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            girar_y_negativo()
            return 2
        if detectar_pared (H_uS_atras)==True and detectar_pared (H_uS_izq)==True:
            # Hay paredes en Y- y X-
            # Gigo a Y-
            girar_y_positivo ()
            time.sleep(1)
            avanzar_linea(vel_busquedaLínea)
            girar_y_negativo ()
            l1=distancia(H_uS_adelante)
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            # Me muevo en el eje  X
            girar_x_positivo ()
            time.sleep(1)
            avanzar_linea(vel_busquedaLínea)
            girar_x_negativo ()
            l1=distancia(H_uS_adelante)
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            girar_y_positivo()
            return 2
        if detectar_pared (H_uS_atras)==True and detectar_pared (H_uS_der)==True:
            # Hay paredes en Y- y X+
            # Gigo a Y-
            girar_y_positivo ()
            time.sleep(1)
            avanzar_linea(vel_busquedaLínea)
            girar_y_negativo ()
            l1=distancia(H_uS_adelante)
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            # Me muevo en el eje  X
            girar_x_negativo ()
            time.sleep(1)
            avanzar_linea(vel_busquedaLínea)
            girar_x_positivo ()
            l1=distancia(H_uS_adelante)
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            girar_y_positivo()
            return 2

    if paredes==3:
        girar_y_positivo ()
        if detectar_pared (H_uS_adelante)==False:
            # No hay pared  en Y+
            # Me muevo en Y
            girar_y_positivo()
            avanzar_linea(vel_busquedaLínea)
            girar_y_negativo ()
            l1=distancia(H_uS_adelante)+0.02
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            # Me muevo en X
            girar_x_positivo ()
            l_adelante=distancia(H_uS_adelante)+0.02
            l_atras=distancia(H_uS_atras)+0.02
            diferencia_distancia=l_adelante-l_atras
            if diferencia_distancia>0:
                # Tengo que avanzar
                l=l_adelante
                avanzar(vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_adelante)
            else:
                # Tengo que retroceder
                l=l_atras
                avanzar(-vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_atras)
            parar()
            girar_y_positivo ()
            return 3
        if detectar_pared (H_uS_atras)==False:
            # No hay pared  en Y-
            # Me muevo en Y
            girar_y_negativo()
            avanzar_linea(vel_busquedaLínea)
            girar_y_positivo ()
            l1=distancia(H_uS_adelante)+0.02
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            # Me muevo en X
            girar_x_positivo ()
            l_adelante=distancia(H_uS_adelante)+0.02
            l_atras=distancia(H_uS_atras)+0.02
            diferencia_distancia=l_adelante-l_atras
            if diferencia_distancia>0:
                # Tengo que avanzar
                l=l_adelante
                avanzar(vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_adelante)
            else:
                # Tengo que retroceder
                l=l_atras
                avanzar(-vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_atras)
            parar()
            girar_y_negativo ()
            return 3        
        if detectar_pared (H_uS_der)==False:
            # No hay pared en X+
            # Me muevo en X
            girar_x_positivo()
            avanzar_linea(vel_busquedaLínea)
            girar_x_negativo ()
            l1=distancia(H_uS_adelante)+0.02
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            # Me muevo en Y
            girar_y_positivo ()
            l_adelante=distancia(H_uS_adelante)+0.02
            l_atras=distancia(H_uS_atras)+0.02
            diferencia_distancia=l_adelante-l_atras
            if diferencia_distancia>0:
                # Tengo que avanzar
                l=l_adelante
                avanzar(vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_adelante)
            else:
                # Tengo que retroceder
                l=l_atras
                avanzar(-vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_atras)
            parar()
            girar_x_positivo () 
            return 3
        if detectar_pared (H_uS_izq)==False:
            # No hay pared en X-
            # Me muevo en X
            girar_x_negativo()
            avanzar_linea(vel_busquedaLínea)
            girar_x_positivo ()
            l1=distancia(H_uS_adelante)+0.02
            l=l1
            avanzar(vel_busquedaLínea)
            while abs((l1/2)-l)>incertidumbre_poscicion:
                l=distancia(H_uS_adelante)
            parar()
            # Me muevo en Y
            girar_y_positivo () 
            l_adelante=distancia(H_uS_adelante)+0.02
            l_atras=distancia(H_uS_atras)+0.02
            diferencia_distancia=l_adelante-l_atras
            if diferencia_distancia>0:
                # Tengo que avanzar
                l=l_adelante
                avanzar(vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_adelante)
            else:
                # Tengo que retroceder
                l=l_atras
                avanzar(-vel_busquedaLínea)
                while ((l_atras+l_adelante)/2)<l:
                    l=distancia(H_uS_atras)
            parar()
            girar_x_negativo () 
            return 3

    if paredes==4:
        # Me muevo en Y
        girar_y_positivo ()
        l_adelante=distancia(H_uS_adelante)+0.02
        l_atras=distancia(H_uS_atras)+0.02
        diferencia_distancia=l_adelante-l_atras
        if diferencia_distancia>0:
            # Tengo que avanzar
            l=l_adelante
            avanzar(vel_busquedaLínea)
            while ((l_atras+l_adelante)/2)<l:
                l=distancia(H_uS_adelante)
        else:
            # Tengo que retroceder
            l=l_atras
            avanzar(-vel_busquedaLínea)
            while ((l_atras+l_adelante)/2)<l:
                l=distancia(H_uS_atras)
        # Me muevo en X
        girar_x_positivo ()
        l_adelante=distancia(H_uS_adelante)+0.02
        l_atras=distancia(H_uS_atras)+0.02
        diferencia_distancia=l_adelante-l_atras
        if diferencia_distancia>0:
            # Tengo que avanzar
            l=l_adelante
            avanzar(vel_busquedaLínea)
            while ((l_atras+l_adelante)/2)<l:
                l=distancia(H_uS_adelante)
        else:
            # Tengo que retroceder
            l=l_atras
            avanzar(-vel_busquedaLínea)
            while ((l_atras+l_adelante)/2)<l:
                l=distancia(H_uS_atras)
        parar()
        girar_y_negativo ()
        return 4
    return 5

#==========================================================
# Función: conectar()
# Descripción: Se conecta al simulador
# Devuelve:   0 -- si no se conecta
#             1 -- si se conecta
#==========================================================
def conectar():
    global clientID, H_floor
    global H_minipi
    global H_rueda_Izq,H_rueda_Der
    global H_uS_adelante, H_uS_atras,H_uS_der,H_uS_izq
    global H_linea_izq, H_linea_C_izq, H_linea_der,H_linea_C_der

    # print ('Comienza el programa')
    # Me conecto al servidor CopelliaSim
    sim.simxFinish(-1)                                          # Me desconecto por las dudas si quedó conectado
    clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,1)  # Me conecto
    #print ('Wait')
    time.sleep(2)

    if clientID==-1:
        print('El server del CoppeliaSim no está conectado')
    # Si es <> de -1 estoy conectado    
    if clientID !=-1:   
	    # Envío que me conecté al V-REP                                         
        print('\n')
        print('CoppeliaSim conectado')
        print('\n')
        sim.simxAddStatusbarMessage(clientID,'Programa conectado',sim.simx_opmode_oneshot)   
        # Comienzo la simulación
        sim.simxStartSimulation(clientID,sim.simx_opmode_oneshot)       

        # Testeo cuantos objetos hay en escena para controlar
        # res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
        # if res==sim.simx_return_ok:
        #     print ('El número de objetos en la escena son: ',len(objs))   
        # else:
        #     print ('No hay objetos a controlar en la escena : ',res)
        #     time.sleep(2)
 	    #=========================================================================================   
        #Obtengo el Handle de la Articulación 0, y si me conecto envío un par de ángulos 
        res1,H_rueda_Izq=sim.simxGetObjectHandle(clientID,'/MiniPi/rueda_Izq',sim.simx_opmode_blocking)
        res2,H_rueda_Der=sim.simxGetObjectHandle(clientID,'/MiniPi/rueda_Der',sim.simx_opmode_blocking)
        res3,H_uS_adelante=sim.simxGetObjectHandle(clientID,'/MiniPi/uS_adelante',sim.simx_opmode_blocking)
        res3,H_uS_atras=sim.simxGetObjectHandle(clientID,'/MiniPi/uS_atras',sim.simx_opmode_blocking)
        res3,H_uS_der=sim.simxGetObjectHandle(clientID,'/MiniPi/uS_der',sim.simx_opmode_blocking)
        res3,H_uS_izq=sim.simxGetObjectHandle(clientID,'/MiniPi/uS_izq',sim.simx_opmode_blocking)
        res4,H_floor=sim.simxGetObjectHandle(clientID,'/Floor',sim.simx_opmode_blocking)
        res5,H_minipi=sim.simxGetObjectHandle(clientID,'/MiniPi',sim.simx_opmode_blocking)
        res6,H_linea_izq=sim.simxGetObjectHandle(clientID,'/MiniPi/linea_Izq',sim.simx_opmode_blocking)
        res7,H_linea_C_izq=sim.simxGetObjectHandle(clientID,'/MiniPi/linea_C_Izq',sim.simx_opmode_blocking)
        res8,H_linea_der=sim.simxGetObjectHandle(clientID,'/MiniPi/linea_Der',sim.simx_opmode_blocking)
        res9,H_linea_C_der=sim.simxGetObjectHandle(clientID,'/MiniPi/linea_C_Der',sim.simx_opmode_blocking)
        if ((res1==sim.simx_return_ok) and (res2==sim.simx_return_ok) and (res3==sim.simx_return_ok) and (res4==sim.simx_return_ok) and (res5==sim.simx_return_ok)
            and (res6==sim.simx_return_ok) and (res7==sim.simx_return_ok) and (res8==sim.simx_return_ok) and (res9==sim.simx_return_ok)):
            print ('Se encontró el manejador de rueda_Izq, el manejador es: ',H_rueda_Izq)
            print ('Se encontró el manejador de rueda_Der, el manejador es: ',H_rueda_Der)
            print ('Se encontró el manejador de los ultra-sonidos, el manejador es: '+str(H_uS_adelante)+','+str(H_uS_atras)+','+str(H_uS_der)+','+str(H_uS_izq))
            print ('Se encontró el manejador del piso: ',H_floor)
            res,eulerAngles=sim.simxGetObjectOrientation(clientID,H_minipi,H_floor,sim.simx_opmode_blocking)
            gama=eulerAngles[2]*180/math.pi
            print ('La orientación del MiniPi es: ',gama)
            return 1
        else:
            print ('Algùn manejador no se encontró.')
            return 0
   
#==========================================================
# Función: desconectar()
# Descripción: Se sdesconecta del simulador
# Devuelve:   
#==========================================================
def desconectar():
    # Paro la simuación
    sim.simxStopSimulation(clientID,sim.simx_opmode_oneshot)
    # Envío que me desconecto al V-REP
    sim.simxAddStatusbarMessage(clientID,'Se desconectó el programa de control Python',sim.simx_opmode_oneshot)
    print('CoppeliaSim se desconectó')
    time.sleep(2)
    sim.simxFinish(clientID)
 
#==========================================================    

def analizarEntorno():
    # Obtener la posición actual del robot
    x, y, z = get_posicion()

    # Obtener las distancias de los ultrasonidos
    distancias = get_distancia_4uS()

    # Analizar las distancias y crear la ´tupla´ (del,atr,der,izq)
    del_result = 1 if distancias[0] != 0 else 0
    atr_result = 1 if distancias[1] != 0 else 0
    der_result = 1 if distancias[2] != 0 else 0
    izq_result = 1 if distancias[3] != 0 else 0

   #return (print('\nEn la posicion(x,y,z):', get_posicion(), '\nHay paredes en (del,atr,der,izq):', (del_result, atr_result, der_result, izq_result)))
   #return(del_result, atr_result, der_result, izq_result)
   
    with open(mapeo, 'a') as archivo:
        archivo.write(','.join(map(str, ((x,y,z),(del_result, atr_result, der_result, izq_result),('\n')))))
   
class Celda:
    
    def __init__(self, coordenadas):
        self.coordenadas = coordenadas
        self.id = self.calcular_id()
        self.norte = 0
        self.sur = 0
        self.este = 0
        self.oeste = 0

    def calcular_id(self):
        # Calcula el ID basado en las coordenadas (fila, columna)
        x, y = self.coordenadas
        return (x - 1) * 5 + y

    def setValores(self, v_norte,  v_sur, v_este, v_oeste):
        self.oeste = v_oeste
        self.este  = v_este
        self.norte = v_norte
        self.sur   = v_sur

def mapear():
    celdaActual = determinar_celda_actual()

    if get_orientacion(DELTA) in ['Y-', 'X-', 'X+', 'Y+']:
        distancias = get_distancia_4uS()

        # Analizar las distancias y crear la tupla (del, atr, der, izq)
        if get_orientacion(DELTA) == 'Y-':
            norte, sur, este, oeste = (1 if d != 0 else 0 for d in distancias)
        elif get_orientacion(DELTA) == 'X-':
            norte, sur, este, oeste = (1 if d != 0 else 0 for d in [distancias[3], distancias[2], distancias[0], distancias[1]])
        elif get_orientacion(DELTA) == 'X+':
            norte, sur, este, oeste = (1 if d != 0 else 0 for d in [distancias[2], distancias[3], distancias[1], distancias[0]])
        elif get_orientacion(DELTA) == 'Y+':
            norte, sur, este, oeste = (1 if d != 0 else 0 for d in [distancias[1], distancias[0], distancias[3], distancias[2]])

        celdaActual.setValores(norte, sur, este, oeste)

        if all(v in [0, 1] for v in [norte, sur, este, oeste]):
            # Formato nuevo: "CXX-Nv-Sv-Ev-Ov"
            with open(mapeo, "a") as archivo:
                archivo.write(f"C{celdaActual.id:02d}-{celdaActual.norte}-{celdaActual.sur}-{celdaActual.este}-{celdaActual.oeste}\n")
        else:
            print(f"Datos inválidos para la celda: {celdaActual.coordenadas}")

    mapa.mapa_tiempo_real(mapeo)

def distancia_a_la_pared():
    return distancia(H_uS_adelante)*100

import mapeo.mapa as mapa

def limpiar_archivo(file_path):
    with open(file_path, 'w') as archivo:
        archivo.write('')

def guardar_mapa_final():
    # Leer los datos del archivo de mapeo actual
    with open(mapeo, 'r') as archivo:
        contenido = archivo.read()
    
    # Guardar el contenido en el archivo de último mapa
    with open(ultimo_mapa, 'w') as archivo:
        archivo.write(contenido)
    
    # Limpiar el archivo de mapeo
    limpiar_archivo(mapeo)
    
def convertir_a_binario(input_path, output_path):
    """
    Convierte el archivo de mapeo en formato texto a formato binario.
    
    Args:
    - input_path: str, la ruta del archivo de entrada (mapeador.txt).
    - output_path: str, la ruta del archivo de salida en formato binario.
    """

    def int_to_bin_str(value, bits):
        """Convierte un entero a una representación binaria de tamaño fijo en formato string."""
        return format(value, f'0{bits}b')

    with open(input_path, "r") as archivo_entrada, open(output_path, "w") as archivo_salida:
        for linea in archivo_entrada:
            # Quitar cualquier espacio o línea nueva sobrante
            linea = linea.strip()

            # Separar la línea en componentes
            partes = linea.split("-")
            numero_celda = int(partes[0][1:])  # Extraer número de celda después de 'C'
            norte = int(partes[1])
            sur = int(partes[2])
            este = int(partes[3])
            oeste = int(partes[4])

            # Convertir los números a binario
            celda_binaria = int_to_bin_str(numero_celda, 5)  # 5 bits para el número de celda
            norte_binario = int_to_bin_str(norte, 1)
            sur_binario = int_to_bin_str(sur, 1)
            este_binario = int_to_bin_str(este, 1)
            oeste_binario = int_to_bin_str(oeste, 1)

            # Concatenar todos los bits y añadir '0' separador
            linea_binaria = f"{celda_binaria}0{norte_binario}{sur_binario}{este_binario}{oeste_binario}"

            # Escribir la línea binaria al archivo de salida
            archivo_salida.write(linea_binaria + "\n")

def obtener_instrucciones():
    print("\nSe detectó un obstáculo. Ingrese nuevas instrucciones:")
    print("1- Avanzar una celda")
    print("2- Girar derecha")
    print("3- Girar izquierda")
    print("4- Centrarse")
    print("Ingrese las acciones separadas por comas (por ejemplo: 1,2,3):")
    return input().strip().split(',')

def ejecuctar_planificacion(lista_de_acciones):
    i = 0  # Índice para la iteración manual de la lista

    mapear()

    while i < len(lista_de_acciones):
        accion, id_accion = lista_de_acciones[i]

        if get_orientacion(5) == 0:
            centrar_orientacion(5)
            mapear()

        if id_accion == 1:  # Si la acción es avanzar_1_celda
            if distancia_a_la_pared() < 20.0 and distancia_a_la_pared() != 0:
                parar()
                # Eliminar las acciones restantes
                lista_de_acciones = lista_de_acciones[:i]

                # Solicitar nuevas instrucciones usando la función encapsulada
                nuevas_instrucciones = obtener_instrucciones()

                for instruccion in nuevas_instrucciones:
                    if instruccion == '1':
                        lista_de_acciones.append((lambda: avanzar_1_celda(VEL_AVANCE), 1))
                    elif instruccion == '2':
                        lista_de_acciones.append((lambda: girar_der(), 2))
                    elif instruccion == '3':
                        lista_de_acciones.append((lambda: girar_izq(), 3))
                    elif instruccion == '4':
                        lista_de_acciones.append((lambda: centrar(), 4))
                    elif instruccion == '5':
                        lista_de_acciones.append((lambda: set_orientacion(), 5))

                # Reiniciar el índice para continuar desde el inicio de las nuevas acciones
                i = 0
                continue

            else:
                accion()  # Ejecutar avanzar_1_celda
                mapear()  # Realizar el mapeo solo si la acción es avanzar_1_celda

        else:
            accion()  # Ejecutar la acción (girar o centrar) sin mapeo

        i += 1

    # Guardar el mapa final y limpiar el archivo de mapeo
    convertir_a_binario(mapeo, binario)
    mapa.mapas_finales(mapeo, ultimo_mapa)
    mapa.superponer_mapas(mapeo, ultimo_mapa)
    guardar_mapa_final()
    desconectar()
    
# Funcion para centrarse automaticamente (solo gira en sentido horario, es un poco tedioso...)
# Utilizar a la hora de ejecutar una planificacion.

def centrar_orientacion(delta):
    res, eulerAngles = sim.simxGetObjectOrientation(clientID, H_minipi, H_floor, sim.simx_opmode_blocking)
    gama = eulerAngles[2] * 180 / math.pi  # Convertimos a grados

    # Definir las orientaciones principales
    orientaciones = {
        'X+': 0,
        'Y+': 90,
        'X-': 180,
        'Y-': 270
    }

    # Corregimos valores negativos para comparación
    if gama < 0:
        gama += 360

    # Encontrar la orientación más cercana
    orientacion_mas_cercana = min(orientaciones, key=lambda x: min(abs(gama - orientaciones[x]), abs(360 - abs(gama - orientaciones[x]))))

    # Calculamos la diferencia entre la orientación actual y la más cercana
    diferencia = min(abs(gama - orientaciones[orientacion_mas_cercana]), abs(360 - abs(gama - orientaciones[orientacion_mas_cercana])))

    # Si la diferencia es mayor que delta, realizamos la corrección
    if diferencia > delta:
        print(f"Corrigiendo orientación desde {gama:.2f}° a {orientaciones[orientacion_mas_cercana]}°")
        # Llamamos a la función que rota el robot para corregir la orientación
        set_orientacion(orientacion_mas_cercana)

        # Esperamos hasta que la orientación esté dentro del margen de error aceptado (delta)
        while diferencia > delta:
            res, eulerAngles = sim.simxGetObjectOrientation(clientID, H_minipi, H_floor, sim.simx_opmode_blocking)
            gama = eulerAngles[2] * 180 / math.pi  # Convertimos a grados nuevamente
            if gama < 0:
                gama += 360
            diferencia = min(abs(gama - orientaciones[orientacion_mas_cercana]), abs(360 - abs(gama - orientaciones[orientacion_mas_cercana])))
        
        print(f"Orientación corregida a {orientaciones[orientacion_mas_cercana]}°")
        parar()  # Detenemos el robot después de corregir la orientación
        return orientacion_mas_cercana
    else:
        print(f"Orientación actual {gama:.2f}° ya está alineada con {orientacion_mas_cercana}")
        return orientacion_mas_cercana

# ==============================
# DETERMINAR CELDA ACTUAL DEL MINIPI
def determinar_x_celda_actual():
    x, _, _ = get_posicion()  # Obtener la posición x real del robot

    # Determinar la celda según el valor de x
    if 1 >= x > 0.6:
        return 1
    elif 0.6 >= x > 0.2:
        return 2
    elif 0.2 >= x > -0.2:
        return 3
    elif -0.2 >= x > -0.6:
        return 4
    elif -0.6 >= x > -1:
        return 5
    else:
        print("FUERA DE RANGO")
        return None  # Retorna None si está fuera de rango

def determinar_y_celda_actual():
    _, y, _ = get_posicion()  # Obtener la posición y real del robot

    # Determinar la celda según el valor de y
    if -1.2 < y <= -0.8:
        return 1
    elif -0.8 < y <= -0.4:
        return 2
    elif -0.4 < y < 0:
        return 3
    elif 0 <= y < 0.4:
        return 4
    elif 0.4 < y < 0.8:
        return 5
    else:
        print("FUERA DE RANGO!")
        return None  # Retorna None si está fuera de rango

# Utiliza las funciones de: determinar_x_celda_actual & determinar_y_celda_actual
def determinar_celda_actual():
    x = determinar_x_celda_actual()
    y = determinar_y_celda_actual()
    
    # Crear una instancia de la clase Celda con el código de la celda
    celda = Celda((x, y))

    return celda

def determinar_celda(celda):

    celda = Celda()
    return (celda.coordenadas())

# ==============================
    