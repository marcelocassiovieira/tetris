import pygame

# Tamaños
COLUMNAS = 10  # tamaño de las columnas
FILAS = 20  # tamaño de las filas
TAMANO_CELDA = 40  # tamaño de las celdas
ANCHO_JUEGO, ALTURA_JUEGO = COLUMNAS * TAMANO_CELDA, FILAS * TAMANO_CELDA  # tamaño del tablero del juego

# Barra lateral
ANCHO_BARRA_LATERAL = 250  # ancho de la barra lateral

# 75% del largo para agregar la puntuacion
FRACCION_ALTURA_PREVISUALIZACION = 0.75
FRACCION_ALTURA_PUNTUACION = 1 - FRACCION_ALTURA_PREVISUALIZACION

# ventana
PADDING = 20
ANCHURA_VENTANA = ANCHO_JUEGO + ANCHO_BARRA_LATERAL + PADDING * 3
ALTURA_VENTANA = ALTURA_JUEGO + PADDING * 2

NEGRO = '#040100'
COLOR_LINEA = '#FFFFFF'
T_COLOR = "#EA0DEA"
O_COLOR = "#FCED06"
J_COLOR = "#0636FC"
L_COLOR = "#FCB906"
I_COLOR = "#06DAFC"
S_COLOR = "#FC2B06"
Z_COLOR = "#3BE138"

# comportamiento del juego
ACTUALIZAR_VELOCIDAD_INICIO = 200
TIEMPO_ESPERA_MOVIMIENTO = 200
TIEMPO_ESPERA_ROTACION = 200

# para que las imagenes aparezcan en el medio del topo de la
# pantalla del juego
BLOQUE_OFFSET = pygame.Vector2(COLUMNAS // 2, -1)


# formas cuando entra a la ventana del juego
TETROMINOS = {
    'T': {'forma': [(0, 0), (-1, 0), (1, 0), (0, -1)], 'color': T_COLOR},
    'O': {'forma': [(0, 0), (0, -1), (1, 0), (1, -1)], 'color': O_COLOR},
    'J': {'forma': [(0, 0), (0, -1), (0, 1), (-1, 1)], 'color': J_COLOR},
    'L': {'forma': [(0, 0), (0, -1), (0, 1), (1, 1)], 'color': L_COLOR},
    'I': {'forma': [(0, 0), (0, -1), (0, -2), (0, 1)], 'color': I_COLOR},
    'S': {'forma': [(0, 0), (-1, 0), (0, -1), (1, -1)], 'color': S_COLOR},
    'Z': {'forma': [(0, 0), (1, 0), (0, -1), (-1, -1)], 'color': Z_COLOR}
}

DATOS_PUNTUACION = {1: 50, 2: 150, 3: 400, 4: 1500}
