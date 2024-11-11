import a_star.a_star as algoritmo
import minipi_lib as robot
import a_star.laberinto as laberinto

laberinto = laberinto.laberinto
VEL_AVANCE = 2
delta = 3  # Ajuste de incertidumbre en orientación

def generar_instrucciones(inicio, destino):
    # Obtener la ruta usando el algoritmo de búsqueda
    
    inicio2 = (inicio[1] - 1, inicio[0] - 1)
    destino2 = (destino[1] - 1, destino[0] - 1) 
    
    ruta = algoritmo.a_star(laberinto, inicio2, destino2)
    
    ruta_ajustada = [(y + 1, x + 1) for x, y in ruta]

    print("Ruta hallada:", ruta_ajustada, '\n')
    
    # Definir las orientaciones
    orientaciones = {
        'N': 'Y-',  # Norte
        'E': 'X+',  # Este
        'S': 'Y+',  # Sur
        'O': 'X-'   # Oeste
    }
    
    # Diccionario para representar las direcciones en términos de movimientos de coordenadas
    movimientos = {
        'N': (-1, 0),  # Norte (y decrementa)
        'E': (0, 1),   # Este (x incrementa)
        'S': (1, 0),   # Sur (y incrementa)
        'O': (0, -1)   # Oeste (x decrementa)
    }
    
    # Función auxiliar para obtener la dirección que debe tomar el robot para avanzar a la siguiente celda
    def obtener_direccion(origen, destino):
        dx, dy = destino[0] - origen[0], destino[1] - origen[1]
        for dir, (mx, my) in movimientos.items():
            if (dx, dy) == (mx, my):
                return dir
        return None

    instrucciones = []
    direccion_actual = None

    # Establecer la orientación inicial y agregarla como la primera instrucción
    if len(ruta) > 1:
        direccion_inicial = obtener_direccion(ruta[0], ruta[1])
        if direccion_inicial:
            orientacion_inicial = orientaciones[direccion_inicial]
            instrucciones.append((lambda: robot.set_orientacion(orientacion_inicial), 5))
            direccion_actual = direccion_inicial

    # Procesar cada celda en la ruta para generar las instrucciones
    for i in range(1, len(ruta)):
        celda_actual = ruta[i - 1]
        siguiente_celda = ruta[i]

        # Determinar la dirección deseada para moverse hacia la siguiente celda
        direccion_deseada = obtener_direccion(celda_actual, siguiente_celda)

        # Si la dirección deseada es diferente a la actual, agregar una instrucción de giro
        if direccion_deseada != direccion_actual:
            if (direccion_actual, direccion_deseada) in [('N', 'E'), ('E', 'S'), ('S', 'O'), ('O', 'N')]:
                instrucciones.append((lambda: robot.girar_der(), 2))  # Giro a la derecha
            elif (direccion_actual, direccion_deseada) in [('N', 'O'), ('O', 'S'), ('S', 'E'), ('E', 'N')]:
                instrucciones.append((lambda: robot.girar_izq(), 3))  # Giro a la izquierda
            elif (direccion_actual, direccion_deseada) in [('N', 'S'), ('S', 'N'), ('E', 'O'), ('O', 'E')]:
                instrucciones.append((lambda: robot.girar_izq(), 3))  # Giro a la izquierda dos veces para dar vuelta
                instrucciones.append((lambda: robot.girar_izq(), 3))
            direccion_actual = direccion_deseada

        # Agregar una instrucción para avanzar una celda
        instrucciones.append((lambda: robot.avanzar_1_celda(VEL_AVANCE), 1))
        
    return instrucciones
