# Fusión de Sensores: Entorno Simulado
**Bryan A. Battagliese - GIAR UTNBA 2024**

## Entorno de Trabajo

Actualmente utilizamos **CoppelliaSIM**, un software de simulación robótica que permite diseñar y probar entornos de simulación complejos de manera rápida y flexible. Cuenta con un motor de simulación distribuida, que permite controlar distintos elementos de una simulación a través de múltiples scripts (como Python, C++, MATLAB). 

En nuestro caso, elegimos **Python** por su facilidad y flexibilidad, además de la amplia variedad de bibliotecas accesibles.

Basado en las premisas del **Robot Planning**, contamos con un espacio estructurado con mosaicos/celdas (en este caso elegimos un tamaño de 5x5). [Fusion de sensores - MINIPI.ttt](path/to/Fusion_de_sensores_MINIPI.ttt).

El robot utilizado es una representación del **MiniPi**. Este cuenta con 4 sensores de ultrasonido (uno en cada cara del cubo); 4 sensores de línea; y un "force-sensor" encargado de mover sus 2 ruedas.  
![MiniPi Componentes](path/to/image1.png)

## Objetivo del Trabajo

El objetivo principal es tener un entorno simulado en el cual el robot MiniPi sea capaz de llegar desde una celda A hasta una celda B, mapeando su entorno y reconociendo paredes/obstáculos a través de sus sensores de ultrasonido. Es importante poder recolectar estos datos y representarlos. 

El MiniPi puede trabajar de diferentes maneras:

### A - Recibiendo instrucciones sobre el camino a realizar

Se le pasa al robot MiniPi una serie de instrucciones simples, que debe ejecutar en serie. Una vez finalizado, muestra lo que pudo mapear (es capaz de mostrar el mapeo en "tiempo real"). 

Las instrucciones simples que entiende nuestro robot son:  
- `avanzar_1_celda`  
- `girar_der`  
- `girar_izq`  
- `centrar`

[Archivo de funciones: minipi_lib.py](path/to/minipi_lib.py)

![Planificación de Instrucciones](path/to/image2.png)
![Simulación Mapeo](path/to/image3.png)

### B - Brindándole solamente la celda destino (en proceso)

El objetivo es que el robot MiniPi reciba solamente la celda a donde debería llegar y lo haga por el "mejor camino".

*Nota:* En cualquiera de los casos, si el MiniPi detecta algún obstáculo o algo que impidiera seguir con su ejecución, se frena y espera que se le indiquen los pasos a seguir desde la consola de desarrollador.

## Información sobre los Archivos del Repositorio

- **Fusion de sensores - MINIPI.ttt**: Es la escena en el simulador CoppelliaSIM.

- **fusion_de_sensores.py**: Es el archivo principal en Python. Aquí se conecta con el simulador y ejecuta lo que se le indique. *(Dentro del "if")*

  *Nota:* Las primeras líneas de código en estos dos programas son variables necesarias, importación de librerías, y obtención de los controladores (handlers) de todos los componentes del robot en el simulador.

- **minipi_lib.py**: Biblioteca de funciones que adaptan las funcionalidades del simulador para poder ser utilizadas en nuestro programa .py.

- **mapa.py**: Programa creado utilizando **Matplotlib**, con el objetivo de mostrar los mapeos realizados por el MiniPi en forma de mapas/laberintos.

- **remoteApi.dll**
- **remoteApi.so**
- **sim.py**
- **simConst.py**

  Estos últimos cuatro son archivos de configuración necesarios para la vinculación del simulador CoppelliaSIM con el programa en Python.

*Nota:* Actualmente se encuentra en desarrollo un algoritmo que permita la búsqueda y ejecución del mejor camino para llegar desde una celda A hasta una celda destino B (caso "B" mencionado anteriormente).
