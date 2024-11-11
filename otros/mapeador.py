import os
import json
import numpy as np

# SE DEFINEN LOS TIPOS DE CELDAS EXISTENTES:

CELL_TYPE                   = dict()
CELL_TYPE["libre"]          = 0
CELL_TYPE["bloquada"]       = 1
CELL_TYPE["unknown"]        = 2
CELL_TYPE["start_north"]    = 3
CELL_TYPE["start_east"]     = 4
CELL_TYPE["start_west"]     = 5
CELL_TYPE["start_south"]    = 6
CELL_TYPE["end_north"]      = 7
CELL_TYPE["end_east"]       = 8
CELL_TYPE["end_west"]       = 9
CELL_TYPE["end_south"]      = 10

###########################################

class Mapeador:

###########################################

    def inicializador(self, nombre, ruta, map_representation):
        self.nombre                 = nombre                       # Nombre del mapeador
        self.ruta                   = ruta                         # Ruta comun utilizada
        self.map_representation     = np.array(map_representation) # Una matriz que representa el mapa
        
        self.estado                 = "Actualizado" # Representa el estado actual del mapeador
        
        self.necesitaActualizarse   = False         # Indicador booleano: si se necesita actualizar el mapa.
        self.mapaActualizado        = False         # Indicador booleano: si el mapa ha sido actualizado.
        self.cambiosEnElMapa        = False         # Indicador booleano: si hubo cambios en el mapa.
        self.nuevasCeldasLibres     = False         # Indicador booleano: si hay nuevas celdas libres.
        self.celdaBloqueadaAdelante = False         # Indicador booleano: si hay una celda bloqueada en frente.

###########################################

    def correrCiclo(self):
        if self.estado == "Actualizado":
            if self.necesitaActualizarse is True:
                self.estado = "Actualizando"
                self.necesitaActualizarse = False
            else:
                self.actualizacionEsNecesaria()
        
        elif self.estado == "Actualizando":
            if self.mapaActualizado is True:
                self.estado = "Actualizado"
                self.mapaActualizado = False
            else:
                self.actualizarMapa()
        
        return self.estado

###########################################
               
    def actualizacionEsNecesaria(self):
        directorio = os.getcwd()

        # Load the common data
        os.chdir(self.ruta)
        with open('background.json') as f:
            background = json.load(f)

        # Check if there is the need for a map update
        if background["necesitaActualizarse"] is True:
            background["necesitaActualizarse"] = False
            self.necesitaActualizarse = True

            # Save the updated common data
            f = open('background.json', 'w')
            json.dump(background, f, sort_keys=True, indent=4)
            f.close()

        os.chdir(directorio)

###########################################
    
    def actualizarMapa(self):
        directorio = os.getcwd()

        # Load the common data
        os.chdir(self.ruta)
        with open('background.json') as f:
            background = json.load(f)

        # Update the map data
        background["map"]           = self.actualizarAgente(background["plan"] [background["current_move"]])
        background["current_move"] += 1
        background["map"]           = self.actualizarAmbiente(background ["sensor_data"])

        # Update the map metadata
        if self.cambiosEnElMapa is True:
            background["nuevasCeldasLibres"] = self.nuevasCeldasLibres
            background["celdaBloqueadaAdelante"] = self.celdaBloqueadaAdelante

        # Save the updated map
        f = open('background.json', 'w')
        json.dump(background, f, sort_keys=True, indent=4)
        f.close()

        # Return setting the status flag
        os.chdir(directorio)
        self.mapaActualizado = True

###########################################
    
    def actualizarAgente(self, move):
        if move == "Get center":
            pass
        elif move == "Go forward":
            if np.where(self.map_representation == CELL_TYPE["start_north"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_north"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_north"])[1]))[0]
                self.map_representation[start[0] - 1][start[1]] = CELL_TYPE["start_north"]
            elif np.where(self.map_representation == CELL_TYPE["start_east"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_east"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_east"])[1]))[0]
                self.map_representation[start[0]][start[1] + 1] = CELL_TYPE["start_east"]
            elif np.where(self.map_representation == CELL_TYPE["start_west"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_west"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_west"])[1]))[0]
                self.map_representation[start[0]][start[1] - 1] = CELL_TYPE["start_west"]
            elif np.where(self.map_representation == CELL_TYPE["start_south"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_south"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_south"])[1]))[0]
                self.map_representation[start[0] + 1][start[1]] = CELL_TYPE["start_south"]
            self.map_representation[start[0]][start[1]] = CELL_TYPE["free"]
        
        elif move == "Turn left":
            if np.where(self.map_representation == CELL_TYPE["start_north"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_north"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_north"])[1]))[0]
                self.map_representation[start[0]][start[1]] = CELL_TYPE["start_west"]
            elif np.where(self.map_representation == CELL_TYPE["start_east"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_east"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_east"])[1]))[0]
                self.map_representation[start[0]][start[1]] = CELL_TYPE["start_north"]
            elif np.where(self.map_representation == CELL_TYPE["start_west"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_west"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_west"])[1]))[0]
                self.map_representation[start[0]][start[1]] = CELL_TYPE["start_south"]
            elif np.where(self.map_representation == CELL_TYPE["start_south"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_south"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_south"])[1]))[0]
                self.map_representation[start[0]][start[1]] = CELL_TYPE["start_east"]
        
        elif move == "Turn right":
            if np.where(self.map_representation == CELL_TYPE["start_north"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_north"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_north"])[1]))[0]
                self.map_representation[start[0]][start[1]] = CELL_TYPE["start_east"]
            elif np.where(self.map_representation == CELL_TYPE["start_east"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_east"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_east"])[1]))[0]
                self.map_representation[start[0]][start[1]] = CELL_TYPE["start_south"]
            elif np.where(self.map_representation == CELL_TYPE["start_west"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_west"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_west"])[1]))[0]
                self.map_representation[start[0]][start[1]] = CELL_TYPE["start_north"]
            elif np.where(self.map_representation == CELL_TYPE["start_south"])[0].size > 0:
                start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_south"])[0],
                                  np.where(self.map_representation == CELL_TYPE["start_south"])[1]))[0]
                self.map_representation[start[0]][start[1]] = CELL_TYPE["start_west"]
        return self.map_representation.tolist()

###########################################
    
    def actualizarAmbiente(self,sensors):
        
        # Obtiene los estados de las celdas que lo rodean
        
        front_cell, right_cell, left_cell, back_cell = \
            CELL_TYPE["free"], CELL_TYPE["free"], CELL_TYPE["free"], CELL_TYPE["free"]
        if sensors["ultrasound_front"] <= 30:
            front_cell = CELL_TYPE["blocked"]
        if sensors["ultrasound_right"] <= 30:
            right_cell = CELL_TYPE["blocked"]
        if sensors["ultrasound_left"] <= 30:
            left_cell = CELL_TYPE["blocked"]
        if sensors["ultrasound_back"] <= 30:
            back_cell = CELL_TYPE["blocked"]

        print(self.map_representation)

        # Check with the map for an agent facing north direction
        if np.where(self.map_representation == CELL_TYPE["start_north"])[0].size > 0:
            start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_north"])[0],
                              np.where(self.map_representation == CELL_TYPE["start_north"])[1]))[0]

            # Check the front cell
            if (self.map_representation[start[0] - 1][start[1]] != CELL_TYPE["blocked"]) and \
                    (front_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.celdaBloqueadaAdelante = True
                self.map_representation[start[0] - 1][start[1]] = front_cell
            elif (self.map_representation[start[0] - 1][start[1]] == CELL_TYPE["blocked"]) and \
                    (front_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0] - 1][start[1]] = front_cell

            # Check the right cell
            if (self.map_representation[start[0]][start[1] + 1] != CELL_TYPE["blocked"]) and \
                    (right_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0]][start[1] + 1] = right_cell
            elif (self.map_representation[start[0]][start[1] + 1] == CELL_TYPE["blocked"]) and \
                    (right_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0]][start[1] + 1] = right_cell

            # Check the left cell
            if (self.map_representation[start[0]][start[1] - 1] != CELL_TYPE["blocked"]) and \
                    (left_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0]][start[1] - 1] = left_cell
            elif (self.map_representation[start[0]][start[1] - 1] == CELL_TYPE["blocked"]) and \
                    (left_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0]][start[1] - 1] = left_cell

            # Check the back cell
            if (self.map_representation[start[0] + 1][start[1]] != CELL_TYPE["blocked"]) and \
                    (back_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0] + 1][start[1]] = back_cell
            elif (self.map_representation[start[0] + 1][start[1]] == CELL_TYPE["blocked"]) and \
                    (back_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0] + 1][start[1]] = back_cell

        # Check with the map for an agent facing east direction
        elif np.where(self.map_representation == CELL_TYPE["start_east"])[0].size > 0:
            start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_east"])[0],
                              np.where(self.map_representation == CELL_TYPE["start_east"])[1]))[0]

            # Check the front cell
            if (self.map_representation[start[0]][start[1] + 1] != CELL_TYPE["blocked"]) and \
                    (front_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.celdaBloqueadaAdelante = True
                self.map_representation[start[0]][start[1] + 1] = front_cell
            elif (self.map_representation[start[0]][start[1] + 1] == CELL_TYPE["blocked"]) and \
                    (front_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0]][start[1] + 1] = front_cell

            # Check the right cell
            if (self.map_representation[start[0] + 1][start[1]] != CELL_TYPE["blocked"]) and \
                    (right_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0] + 1][start[1]] = right_cell
            elif (self.map_representation[start[0] + 1][start[1]] == CELL_TYPE["blocked"]) and \
                    (right_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0] + 1][start[1]] = right_cell

            # Check the left cell
            if (self.map_representation[start[0] - 1][start[1]] != CELL_TYPE["blocked"]) and \
                    (left_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0] - 1][start[1]] = left_cell
            elif (self.map_representation[start[0] - 1][start[1]] == CELL_TYPE["blocked"]) and \
                    (left_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0] - 1][start[1]] = left_cell

            # Check the back cell
            if (self.map_representation[start[0]][start[1] - 1] != CELL_TYPE["blocked"]) and \
                    (back_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0]][start[1] - 1] = back_cell
            elif (self.map_representation[start[0]][start[1] - 1] == CELL_TYPE["blocked"]) and \
                    (back_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0]][start[1] - 1] = back_cell

        # Check with the map for an agent facing west direction
        elif np.where(self.map_representation == CELL_TYPE["start_west"])[0].size > 0:
            start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_west"])[0],
                              np.where(self.map_representation == CELL_TYPE["start_west"])[1]))[0]

            # Check the front cell
            if (self.map_representation[start[0]][start[1] - 1] != CELL_TYPE["blocked"]) and \
                    (front_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.celdaBloqueadaAdelante = True
                self.map_representation[start[0]][start[1] - 1] = front_cell
            elif (self.map_representation[start[0]][start[1] - 1] == CELL_TYPE["blocked"]) and \
                    (front_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0]][start[1] - 1] = front_cell

            # Check the right cell
            if (self.map_representation[start[0] - 1][start[1]] != CELL_TYPE["blocked"]) and \
                    (right_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0] - 1][start[1]] = right_cell
            elif (self.map_representation[start[0] - 1][start[1]] == CELL_TYPE["blocked"]) and \
                    (right_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0] - 1][start[1]] = right_cell

            # Check the left cell
            if (self.map_representation[start[0] + 1][start[1]] != CELL_TYPE["blocked"]) and \
                    (left_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0] + 1][start[1]] = left_cell
            elif (self.map_representation[start[0] + 1][start[1]] == CELL_TYPE["blocked"]) and \
                    (left_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0] + 1][start[1]] = left_cell

            # Check the back cell
            if (self.map_representation[start[0]][start[1] + 1] != CELL_TYPE["blocked"]) and \
                    (back_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0]][start[1] + 1] = back_cell
            elif (self.map_representation[start[0]][start[1] + 1] == CELL_TYPE["blocked"]) and \
                    (back_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0]][start[1] + 1] = back_cell

        # Check with the map for an agent facing south direction
        elif np.where(self.map_representation == CELL_TYPE["start_south"])[0].size > 0:
            start = tuple(zip(np.where(self.map_representation == CELL_TYPE["start_south"])[0],
                              np.where(self.map_representation == CELL_TYPE["start_south"])[1]))[0]

            # Check the front cell
            if (self.map_representation[start[0] + 1][start[1]] != CELL_TYPE["blocked"]) and \
                    (front_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.celdaBloqueadaAdelante = True
                self.map_representation[start[0] + 1][start[1]] = front_cell
            elif (self.map_representation[start[0] + 1][start[1]] == CELL_TYPE["blocked"]) and \
                    (front_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0] + 1][start[1]] = front_cell

            # Check the right cell
            if (self.map_representation[start[0]][start[1] - 1] != CELL_TYPE["blocked"]) and \
                    (right_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0]][start[1] - 1] = right_cell
            elif (self.map_representation[start[0]][start[1] - 1] == CELL_TYPE["blocked"]) and \
                    (right_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0]][start[1] - 1] = right_cell

            # Check the left cell
            if (self.map_representation[start[0]][start[1] + 1] != CELL_TYPE["blocked"]) and \
                    (left_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0]][start[1] + 1] = left_cell
            elif (self.map_representation[start[0]][start[1] + 1] == CELL_TYPE["blocked"]) and \
                    (left_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0]][start[1] + 1] = left_cell

            # Check the back cell
            if (self.map_representation[start[0] - 1][start[1]] != CELL_TYPE["blocked"]) and \
                    (back_cell == CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.map_representation[start[0] - 1][start[1]] = back_cell
            elif (self.map_representation[start[0] - 1][start[1]] == CELL_TYPE["blocked"]) and \
                    (back_cell != CELL_TYPE["blocked"]):
                self.cambiosEnElMapa = True
                self.nuevasCeldasLibres = True
                self.map_representation[start[0] - 1][start[1]] = back_cell

        print(self.map_representation)

        return self.map_representation.tolist()

###########################################

if __name__ == "__main__":
    pass


# DUDAS

# No entiendo como es la relacion con los .json