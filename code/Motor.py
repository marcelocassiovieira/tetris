from Constantes import *
from sys import exit
from os.path import join

# components
from Juego import Juego
from Puntaje import Puntaje
from Previsualizacion import Previsualizacion
from random import choice


class Motor:
    def __init__(self):

        # general
        pygame.init()
        self.mostrar = pygame.display.set_mode((ANCHURA_VENTANA, ALTURA_VENTANA))
        self.reloj = pygame.time.Clock()
        pygame.display.set_caption('Paradigmas 2023 - Tetris')

        # formas - obtengo las 3 formas que llenan la previsualizacion
        self.siguientes_formas = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # componentes
        self.juego = Juego(self.obtener_proxima_figura, self.actulizar_puntos)
        self.puntaje = Puntaje()
        self.previsualizacion = Previsualizacion()

        # audio
        self.musica = pygame.mixer.Sound(join('..', 'sonidos', 'music.mp3'))
        self.musica.set_volume(0.1)
        self.musica.play(-1)

    def actulizar_puntos(self, lines, score, level):
        self.puntaje.lines = lines
        self.puntaje.score = score
        self.puntaje.level = level

    def obtener_proxima_figura(self):
        proxima_forma = self.siguientes_formas.pop(0)
        self.siguientes_formas.append(choice(list(TETROMINOS.keys())))
        return proxima_forma

    def ejecutar(self):
        while True:
            # Agrego el evento para cerrar la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Salgo de todo el juego

            # mostrar pantalla - Define el color de la pantalla
            self.mostrar.fill(NEGRO)

            # # componentes
            self.juego.ejecutar()
            self.puntaje.ejecutar()
            self.previsualizacion.ejecutar(self.siguientes_formas)
            #
            # actualizar juego
            pygame.display.update()
            self.reloj.tick()
