from Constantes import *
from pygame.image import load
from os import path


class Previsualizacion:
    def __init__(self):
        # general
        self.mostrar_superficie = pygame.display.get_surface()
        self.superficie = pygame.Surface((ANCHO_BARRA_LATERAL, ALTURA_JUEGO * FRACCION_ALTURA_PREVISUALIZACION))
        self.rect = self.superficie.get_rect(topright=(ANCHURA_VENTANA - PADDING, PADDING))

        # shapes
        self.forma_superficie = {shape: load(path.join('..', 'graficos', f'{shape}.png')).convert_alpha() for shape in
                                 TETROMINOS.keys()}

        # image position data
        self.incrementar_altura = self.superficie.get_height() / 3

    def mostrar_piezas(self, piezas):
        for i, pieza in enumerate(piezas):
            forma_superficie = self.forma_superficie[pieza]
            x = self.superficie.get_width() / 2
            y = self.incrementar_altura / 2 + i * self.incrementar_altura
            recta = forma_superficie.get_rect(center=(x, y))
            self.superficie.blit(forma_superficie, recta)

    def ejecutar(self, proxima_pieza):
        self.superficie.fill(NEGRO)
        self.mostrar_piezas(proxima_pieza)
        self.mostrar_superficie.blit(self.superficie, self.rect)
        pygame.draw.rect(self.mostrar_superficie, COLOR_LINEA, self.rect, 2, 2)
