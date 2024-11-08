laberinto = {
    
    # fila 1 ->
    (0, 0): {"norte": True, "sur": False, "este": True,  "oeste": True},
    (0, 1): {"norte": True, "sur": True , "este": False, "oeste": True},
    (0, 2): {"norte": True, "sur": True, "este": False, "oeste": False},
    (0, 3): {"norte": True, "sur": False, "este": False, "oeste": False},
    (0, 4): {"norte": True, "sur": True , "este": True, "oeste": False},
    
    # fila 2 ->
    (1, 0): {"norte": False, "sur": False, "este": False, "oeste":True },
    (1, 1): {"norte": True,  "sur": True, "este": False, "oeste": False},
    (1, 2): {"norte": True,  "sur": True, "este": True, "oeste": False},
    (1, 3): {"norte": False, "sur": False, "este": True, "oeste":True},
    (1, 4): {"norte": True, "sur": False , "este": True, "oeste": True},
    
    # fila 3 ->
    (2, 0): {"norte": False, "sur": False, "este": True, "oeste": True},
    (2, 1): {"norte": True, "sur": False, "este": False, "oeste": True},
    (2, 2): {"norte": True, "sur": False, "este": False, "oeste": False },
    (2, 3): {"norte": False, "sur": True, "este": False, "oeste": False },
    (2, 4): {"norte": False, "sur": False, "este": True, "oeste":False },
    
    # fila 4 ->
    (3, 0): {"norte": False, "sur": False, "este": False, "oeste": True},
    (3, 1): {"norte": False , "sur": True, "este": True, "oeste": False},
    (3, 2): {"norte": False, "sur": False, "este":True, "oeste": True},
    (3, 3): {"norte": True, "sur": True, "este": True, "oeste":True },
    (3, 4): {"norte": False, "sur": False, "este": True, "oeste": True},
    
    # fila 5 ->
    (4, 0): {"norte": False, "sur": True, "este": False, "oeste": True},
    (4, 1): {"norte": True, "sur": True, "este": True, "oeste": False},
    (4, 2): {"norte": False, "sur": True, "este":False , "oeste": True},
    (4, 3): {"norte": True, "sur": True, "este": True, "oeste": False},
    (4, 4): {"norte": False, "sur": True, "este": True, "oeste": True},
    
}
