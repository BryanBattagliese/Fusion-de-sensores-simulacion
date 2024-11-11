# """ """ """ """ """ """ """ """ """ """ """ """ #                                              
# UNIVERSIDAD TECNOLOGICA NACIONAL FRBA           #
# GRUPO INTELIGENCIA ARTIFICIAL Y ROBOTICA (GIAR) #
#                                                 #  
# "Fusion de sensores en ambiente estructurado"   #                                           
#               -ENTORNO SIMULADO-                #
#                                                 #
# Bryan A. Battagliese Montiel                    #                          
# 2024                                            #  
#                                                 #  
# """ """ """ """ """ """ """ """ """ """ """ """ #                                              

import sim
import simConst
import time
import math
import numpy as np
import minipi_lib as robot
import mapeo.mapa as mapa
import a_star.a_star_adapter as adapter

#========================================================
#                       Constantes
#========================================================

VEL_BUSQUEDALINEA = 1.5       # Velocidad baja 1.5
VEL_AVANCE = 2
VEL_GIRO_DIRECCION = 1      # Es la velocidad con que gira
GRADOS_INCERTIDUMBRE = 1      # 0.5º
GRADOS_INCERDIDUMBRE_CONSULTA = 5
POS_INCERTIDUMBRE = 0.05      # 0,4 cm
LONG_CELDA = 0.4              # La longitud de la celda es de 40cm
DELTA = 3

#========================================================
#                      Variables globales
#========================================================

# Handle del entorno CoppeliaSim
clientID = 0      

# Handle del piso
H_floor  = 0       
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

#========================================================
#                 Programa principal
#========================================================

if robot.conectar():
    
   time.sleep(2)

#========================================================

   inicio = (1,1)
   final  = (2,3)
   
   planificacion  = adapter.generar_instrucciones(inicio, final)
   
   robot.ejecuctar_planificacion(planificacion)

#========================================================
   time.sleep(2)
   robot.desconectar()
       
else:
    print('No se pudo conectar')
    
	#=========================================================================================  
    # Paro la simuación
    
    sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot)
    # Envío que me desconecto al V-REP
    
    sim.simxAddStatusbarMessage(clientID, 'Se desconectó el programa de control Python', sim.simx_opmode_oneshot)
    print('CoppeliaSim se desconectó')
    time.sleep(2)
    sim.simxFinish(clientID)
