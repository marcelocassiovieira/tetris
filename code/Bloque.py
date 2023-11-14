from Constantes import *


class Bloque(pygame.sprite.Sprite):
    def __init__(self, grupo, pos, color):
        # general
        super().__init__(grupo)
        self.image = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA))
        self.image.fill(color)
        # position
        self.posicion = pygame.Vector2(pos) + BLOQUE_OFFSET
        self.rect = self.image.get_rect(topleft=self.posicion * TAMANO_CELDA)

    # Roto las piezas tetrominos
    def rotar(self, posicion_pivot):
        return posicion_pivot + (self.posicion - posicion_pivot).rotate(90)

    # actualiza la posicion de la imagen en la grilla del juego
    def update(self):
        self.rect.topleft = self.posicion * TAMANO_CELDA

    def colision_horizontal(self, x, data):
        if not 0 <= x < COLUMNAS:
            return True
        if data[int(self.posicion.y)][x]:
            return True

    def colision_vertical(self, y, data):
        if y >= FILAS:
            return True
        if y >= 0 and data[y][int(self.posicion.x)]:
            return True
