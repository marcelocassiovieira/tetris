from Constantes import *
from os.path import join


class Puntaje:
    def __init__(self):
        self.superficie = pygame.Surface((ANCHO_BARRA_LATERAL, ALTURA_JUEGO * FRACCION_ALTURA_PUNTUACION - PADDING))
        self.rect = self.superficie.get_rect(bottomright=(ANCHURA_VENTANA - PADDING, ALTURA_VENTANA - PADDING))
        self.mostrar_superficie = pygame.display.get_surface()

        # fuente
        self.fuente = pygame.font.Font(join('..', 'graficos', 'Russo_One.ttf'), 30)

        # incrementar altura
        self.incrementar_altura = self.superficie.get_height() / 3

        # data
        self.puntuacion = 0
        self.nivel = 1
        self.lineas = 0

    def mostrar_texto(self, pos, text):
        texto_superficie = self.fuente.render(f'{text[0]}: {text[1]}', True, 'white')
        texto_rect = texto_superficie.get_rect(center=pos)
        self.superficie.blit(texto_superficie, texto_rect)

    def ejecutar(self):
        self.superficie.fill(NEGRO)
        for i, text in enumerate([('Puntaje', self.puntuacion), ('Nivel', self.nivel), ('Lineas', self.lineas)]):
            x = self.superficie.get_width() / 2
            y = self.incrementar_altura / 2 + i * self.incrementar_altura
            self.mostrar_texto((x, y), text)

        self.mostrar_superficie.blit(self.superficie, self.rect)
        pygame.draw.rect(self.mostrar_superficie, COLOR_LINEA, self.rect, 2, 2)
