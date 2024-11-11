import heapq
import a_star.laberinto as laberinto

laberinto = laberinto.laberinto

def heuristica(celda_actual, celda_objetivo):
    return abs(celda_actual[0] - celda_objetivo[0]) + abs(celda_actual[1] - celda_objetivo[1])

def vecinos(celda, laberinto):
    x, y = celda
    posibles_movimientos = []
    if not laberinto[celda]["norte"]:
        posibles_movimientos.append((x - 1, y))  # Norte
    if not laberinto[celda]["sur"]:
        posibles_movimientos.append((x + 1, y))  # Sur
    if not laberinto[celda]["este"]:
        posibles_movimientos.append((x, y + 1))  # Este
    if not laberinto[celda]["oeste"]:
        posibles_movimientos.append((x, y - 1))  # Oeste
    # Filtra movimientos fuera de límites
    return [mov for mov in posibles_movimientos if 0 <= mov[0] < 5 and 0 <= mov[1] < 5]

def a_star(laberinto, inicio, objetivo):
    # Estructuras para nodos abiertos y cerrados
    abiertos = []
    heapq.heappush(abiertos, (0, inicio))
    costos = {inicio: 0}
    camino = {inicio: None}
    
    while abiertos:
        _, celda_actual = heapq.heappop(abiertos)
        
        if celda_actual == objetivo:
            # Reconstruir camino desde el objetivo
            ruta = []
            while celda_actual:
                ruta.append(celda_actual)
                celda_actual = camino[celda_actual]
            return ruta[::-1]  # Regresar el camino en orden inverso
        
        for vecino in vecinos(celda_actual, laberinto):
            nuevo_costo = costos[celda_actual] + 1  # Asume costo 1 por cada paso
            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                prioridad = nuevo_costo + heuristica(vecino, objetivo)
                heapq.heappush(abiertos, (prioridad, vecino))
                camino[vecino] = celda_actual
    
    
    print("Ruta encontrada:", ruta)
           
    return None  # No se encontró camino
