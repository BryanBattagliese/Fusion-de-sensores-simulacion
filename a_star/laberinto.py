laberinto = {
    
    # fila 1 ->
    (0, 0): {"norte": True, "sur": False, "este": True,  "oeste": True},        # Celda 1
    (0, 1): {"norte": True, "sur": True , "este": False, "oeste": True},        # Celda 6
    (0, 2): {"norte": True, "sur": True, "este": False, "oeste": False},        # Celda 11
    (0, 3): {"norte": True, "sur": False, "este": False, "oeste": False},       # Celda 16
    (0, 4): {"norte": True, "sur": True , "este": True, "oeste": False},        # Celda 21
    
    # fila 2 ->
    (1, 0): {"norte": False, "sur": False, "este": False, "oeste":True },       # Celda 2
    (1, 1): {"norte": True,  "sur": True, "este": False, "oeste": False},       # Celda 7
    (1, 2): {"norte": True,  "sur": True, "este": True, "oeste": False},        # Celda 12
    (1, 3): {"norte": False, "sur": False, "este": True, "oeste":True},         # Celda 17
    (1, 4): {"norte": True, "sur": False , "este": True, "oeste": True},        # Celda 22
    
    # fila 3 ->
    (2, 0): {"norte": False, "sur": False, "este": True, "oeste": True},        # Celda 3
    (2, 1): {"norte": True, "sur": False, "este": False, "oeste": True},        # Celda 8
    (2, 2): {"norte": True, "sur": False, "este": False, "oeste": False },      # Celda 13
    (2, 3): {"norte": False, "sur": True, "este": False, "oeste": False },      # Celda 18
    (2, 4): {"norte": False, "sur": False, "este": True, "oeste":False },       # Celda 23

    # fila 4 ->
    (3, 0): {"norte": False, "sur": False, "este": False, "oeste": True},       # Celda 4
    (3, 1): {"norte": False , "sur": True, "este": True, "oeste": False},       # Celda 9
    (3, 2): {"norte": False, "sur": False, "este":True, "oeste": True},         # Celda 14
    (3, 3): {"norte": True, "sur": True, "este": True, "oeste":True },          # Celda 19
    (3, 4): {"norte": False, "sur": False, "este": True, "oeste": True},        # Celda 24    
    
    # fila 5 ->
    (4, 0): {"norte": False, "sur": True, "este": False, "oeste": True},        # Celda 5
    (4, 1): {"norte": True, "sur": True, "este": True, "oeste": False},         # Celda 10
    (4, 2): {"norte": False, "sur": True, "este":False , "oeste": True},        # Celda 15
    (4, 3): {"norte": True, "sur": True, "este": True, "oeste": False},         # Celda 20
    (4, 4): {"norte": False, "sur": True, "este": True, "oeste": True},         # Celda 25
    
}