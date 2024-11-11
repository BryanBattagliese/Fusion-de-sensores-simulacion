import matplotlib.pyplot as plt
import time
import a_star.laberinto as laberinto

def id_to_coordinates(id_part):
    # Nueva distribución: celdas en columnas
    col = (id_part - 1) // 5 + 1  # Determina la columna
    row = (id_part - 1) % 5 + 1   # Determina la fila
    return row, col

def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("C"):
            parts = line.split('-')
            id_part = int(parts[0].strip('C'))
            north = int(parts[1])
            south = int(parts[2])
            east = int(parts[3])
            west = int(parts[4])

            # Convertir el id en coordenadas (fila, columna) según la nueva distribución
            # La columna corresponde a id_part % 5, y la fila se obtiene de id_part // 5
            col = (id_part - 1) // 5 + 1  # Se obtiene con la división entera (id_part - 1) // 5
            row = (id_part - 1) % 5 + 1   # Se invierte el módulo para las filas

            # Invertir fila y columna para que coincida con el nuevo esquema
            item = {
                "coordenadas": [col, row],  # Ajustado para reflejar la nueva estructura
                "norte": north,
                "sur": south,
                "este": east,
                "oeste": west
            }
            data.append(item)

    return data

def mapa_tiempo_real(file_path):
    # Función para leer el archivo y convertir los datos en una lista de diccionarios

    # Leer los datos del archivo
    data = read_data_from_file(file_path)

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Ajustar el eje
    ax.set_xlim(0, 5)
    ax.set_ylim(5, 0)  # Invertir el eje y
    ax.set_aspect('equal')

    # Ocultar los ejes
    ax.axis('off')

    # Añadir un título
    ax.set_title('MAPEO EN EJECUCION ...', fontsize=16, fontweight='bold', pad=20)


    for index, item in enumerate(data):
        x, y = item['coordenadas'][0] - 1, item['coordenadas'][1] - 1
        north = item['norte']
        south = item['sur']
        east = item['este']
        west = item['oeste']
        
        # Dibujar paredes norte
        if north == 1:
            ax.plot([x, x + 1], [y, y], color='red', linewidth=5, linestyle='-')
        else:
            ax.plot([x, x + 1], [y, y], color='black', linestyle='--')
        
        # Dibujar paredes sur
        if south == 1:
            ax.plot([x, x + 1], [y + 1, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax.plot([x, x + 1], [y + 1, y + 1], color='black', linestyle='--')
        
        # Dibujar paredes este
        if east == 1:
            ax.plot([x + 1, x + 1], [y, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax.plot([x + 1, x + 1], [y, y + 1], color='black', linestyle='--')
        
        # Dibujar paredes oeste
        if west == 1:
            ax.plot([x, x], [y, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax.plot([x, x], [y, y + 1], color='black', linestyle='--')
        
        # Añadir el ID de la celda en el medio
        ax.text(x + 0.5, y + 0.5, f'{item["coordenadas"][0]},{item["coordenadas"][1]}', 
                ha='center', va='center', fontsize=6)

        # Mostrar la celda actual
        plt.draw()
        
        # Pausar para cada celda excepto la última
        if index < len(data) - 1:
            plt.pause(0.5)  # Mostrar más rápido cada celda, reducir el tiempo a 0.5 segundos
        else:
            plt.pause(3)  # Mantener la última celda en pantalla por 2 segundos

    # Cerrar la ventana automáticamente después de la última pausa
    plt.close()

def mapas_finales(file_path_anterior, file_path_final):
    # Leer los datos de ambos archivos
    data_final = read_data_from_file(file_path_anterior)
    data_anterior = read_data_from_file(file_path_final)

    # Crear una figura con dos subplots uno al lado del otro
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Ajustar el espacio entre subplots
    fig.subplots_adjust(wspace=0.2)  # Incrementa el espacio entre subplots para dar más espacio a la línea divisoria

    # --- Mapa FINAL ---
    ax1.set_title('MAPEO ACTUAL FINALIZADO', fontsize=16, fontweight='bold', pad=20, loc='center')
    ax1.set_xlim(0, 5)
    ax1.set_ylim(5, 0)  # Invertir el eje y
    ax1.set_aspect('equal')
    ax1.axis('off')

    for item in data_final:
        x, y = item['coordenadas'][0] - 1, item['coordenadas'][1] - 1
        north = item['norte']
        south = item['sur']
        east = item['este']
        west = item['oeste']
        
        # Dibujar paredes norte
        if north == 1:
            ax1.plot([x, x + 1], [y, y], color='red', linewidth=5, linestyle='-')
        else:
            ax1.plot([x, x + 1], [y, y], color='black', linestyle='--')
        
        # Dibujar paredes sur
        if south == 1:
            ax1.plot([x, x + 1], [y + 1, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax1.plot([x, x + 1], [y + 1, y + 1], color='black', linestyle='--')
        
        # Dibujar paredes este
        if east == 1:
            ax1.plot([x + 1, x + 1], [y, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax1.plot([x + 1, x + 1], [y, y + 1], color='black', linestyle='--')
        
        # Dibujar paredes oeste
        if west == 1:
            ax1.plot([x, x], [y, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax1.plot([x, x], [y, y + 1], color='black', linestyle='--')
        
        # Añadir el ID de la celda en el medio
        ax1.text(x + 0.5, y + 0.5, f'{item["coordenadas"][0]},{item["coordenadas"][1]}', 
                 ha='center', va='center', fontsize=6)

    # --- Mapa ANTERIOR ---
    ax2.set_title('MAPEO ANTERIOR', fontsize=16, fontweight='bold', pad=20, loc='center')
    ax2.set_xlim(0, 5)
    ax2.set_ylim(5, 0)  # Invertir el eje y
    ax2.set_aspect('equal')
    ax2.axis('off')

    for item in data_anterior:
        x, y = item['coordenadas'][0] - 1, item['coordenadas'][1] - 1
        north = item['norte']
        south = item['sur']
        east = item['este']
        west = item['oeste']
        
        # Dibujar paredes norte
        if north == 1:
            ax2.plot([x, x + 1], [y, y], color='red', linewidth=5, linestyle='-')
        else:
            ax2.plot([x, x + 1], [y, y], color='black', linestyle='--')
        
        # Dibujar paredes sur
        if south == 1:
            ax2.plot([x, x + 1], [y + 1, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax2.plot([x, x + 1], [y + 1, y + 1], color='black', linestyle='--')
        
        # Dibujar paredes este
        if east == 1:
            ax2.plot([x + 1, x + 1], [y, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax2.plot([x + 1, x + 1], [y, y + 1], color='black', linestyle='--')
        
        # Dibujar paredes oeste
        if west == 1:
            ax2.plot([x, x], [y, y + 1], color='red', linewidth=5, linestyle='-')
        else:
            ax2.plot([x, x], [y, y + 1], color='black', linestyle='--')
        
        # Añadir el ID de la celda en el medio
        ax2.text(x + 0.5, y + 0.5, f'{item["coordenadas"][0]},{item["coordenadas"][1]}', 
                 ha='center', va='center', fontsize=6)

    # Añadir una línea divisoria entre los dos subplots, pero sin superponer
    divider = plt.Line2D([0.51, 0.51], [0.1, 0.9], transform=fig.transFigure, color="gray", linewidth=2)
    fig.add_artist(divider)

    # Mostrar ambos mapas en la misma ventana
    plt.show()

def superponer_mapas(file_path_anterior, file_path_final):
    # Leer los datos de ambos archivos
    data_final = read_data_from_file(file_path_final)
    data_anterior = read_data_from_file(file_path_anterior)

    # Crear una figura para un único mapa
    fig, ax = plt.subplots(figsize=(6, 6))

    # Ajustar el eje
    ax.set_xlim(0, 5)
    ax.set_ylim(5, 0)  # Invertir el eje y
    ax.set_aspect('equal')
    ax.axis('off')

    ax.set_title('MAPA SUPERPUESTO', fontsize=16, fontweight='bold', pad=20)

    # Comparar y dibujar las paredes
    for item_anterior, item_final in zip(data_anterior, data_final):
        x, y = item_anterior['coordenadas'][0] - 1, item_anterior['coordenadas'][1] - 1

        # Comparar y dibujar paredes norte
        if item_anterior['norte'] != item_final['norte']:
            if item_final['norte'] == 1:
                ax.plot([x, x + 1], [y, y], color='blue', linewidth=5)  # Nueva pared en azul
            else:
                ax.plot([x, x + 1], [y, y], color='blue', linewidth=1, linestyle='--')  # Pared eliminada en azul punteado
        else:
            color = 'red' if item_final['norte'] == 1 else 'black'
            ax.plot([x, x + 1], [y, y], color=color, linewidth=5 if item_final['norte'] == 1 else 1)

        # Comparar y dibujar paredes sur
        if item_anterior['sur'] != item_final['sur']:
            if item_final['sur'] == 1:
                ax.plot([x, x + 1], [y + 1, y + 1], color='blue', linewidth=5)
            else:
                ax.plot([x, x + 1], [y + 1, y + 1], color='blue', linewidth=1, linestyle='--')
        else:
            color = 'red' if item_final['sur'] == 1 else 'black'
            ax.plot([x, x + 1], [y + 1, y + 1], color=color, linewidth=5 if item_final['sur'] == 1 else 1)

        # Comparar y dibujar paredes este
        if item_anterior['este'] != item_final['este']:
            if item_final['este'] == 1:
                ax.plot([x + 1, x + 1], [y, y + 1], color='blue', linewidth=5)
            else:
                ax.plot([x + 1, x + 1], [y, y + 1], color='blue', linewidth=1, linestyle='--')
        else:
            color = 'red' if item_final['este'] == 1 else 'black'
            ax.plot([x + 1, x + 1], [y, y + 1], color=color, linewidth=5 if item_final['este'] == 1 else 1)

        # Comparar y dibujar paredes oeste
        if item_anterior['oeste'] != item_final['oeste']:
            if item_final['oeste'] == 1:
                ax.plot([x, x], [y, y + 1], color='blue', linewidth=5)
            else:
                ax.plot([x, x], [y, y + 1], color='blue', linewidth=1, linestyle='--')
        else:
            color = 'red' if item_final['oeste'] == 1 else 'black'
            ax.plot([x, x], [y, y + 1], color=color, linewidth=5 if item_final['oeste'] == 1 else 1)

        # Añadir el ID de la celda en el medio
        ax.text(x + 0.5, y + 0.5, f'{item_anterior["coordenadas"][0]},{item_anterior["coordenadas"][1]}', 
                ha='center', va='center', fontsize=6)

    # Mostrar el mapa superpuesto
    plt.show()
