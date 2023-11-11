from Constantes import *
from random import choice
from sys import exit
from os.path import join
from Tretomino import Tetromino
from Temporizador import Temporizador


class Juego:
    def __init__(self, obtener_proxima_forma, actualizar_puntaje):

        # general
        self.superficie = pygame.Surface((ANCHO_JUEGO, ALTURA_JUEGO))
        self.mostrar_superficie = pygame.display.get_surface()
        self.rect = self.superficie.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # game connection
        self.obtener_proxima_forma = obtener_proxima_forma
        self.actualizar_puntaje = actualizar_puntaje

        # lines
        self.superficile_linea = self.superficie.copy()
        self.superficile_linea.fill((0, 255, 0))
        self.superficile_linea.set_colorkey((0, 255, 0))
        self.superficile_linea.set_alpha(120)

        # tetromino
        self.data = [[0 for x in range(COLUMNAS)] for y in range(FILAS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.crear_nuevo_tetromino,
            self.data)

        # timer
        self.down_speed = ACTUALIZAR_VELOCIDAD_INICIO
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Temporizador(self.down_speed, True, self.move_down),
            'horizontal move': Temporizador(TIEMPO_ESPERA_MOVIMIENTO),
            'rotate': Temporizador(TIEMPO_ESPERA_ROTACION)
        }
        self.timers['vertical move'].activar()

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

        # sound
        self.landing_sound = pygame.mixer.Sound(join('..', 'sonidos', 'landing.wav'))
        self.landing_sound.set_volume(0.1)

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += DATOS_PUNTUACION[num_lines] * self.current_level

        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.down_speed_faster = self.down_speed * 0.3
            self.timers['vertical move'].duracion = self.down_speed

        self.actualizar_puntaje(self.current_lines, self.current_score, self.current_level)

    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.posicion.y < 0:
                exit()

    def crear_nuevo_tetromino(self):
        self.landing_sound.play()
        self.check_game_over()
        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.obtener_proxima_forma(),
            self.sprites,
            self.crear_nuevo_tetromino,
            self.data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.actualizar()

    def move_down(self):
        self.tetromino.move_down()

    # Entrada de teclado del usuario
    def entrada(self):
        keys = pygame.key.get_pressed()

        # checking horizontal movement
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activar()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activar()

        # check for rotation
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activar()

        # down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duracion = self.down_speed_faster

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duracion = self.down_speed

    def check_finished_rows(self):

        # get the full row indexes
        borrar_filas = []
        for i, row in enumerate(self.data):
            if all(row):
                borrar_filas.append(i)

        if borrar_filas:
            for delete_row in borrar_filas:

                # delete full rows
                for block in self.data[delete_row]:
                    block.kill()

                # move down blocks
                for row in self.data:
                    for block in row:
                        if block and block.posicion.y < delete_row:
                            block.posicion.y += 1

            # rebuild the field data
            self.data = [[0 for x in range(COLUMNAS)] for y in range(FILAS)]
            for block in self.sprites:
                self.data[int(block.posicion.y)][int(block.posicion.x)] = block

            # update score
            self.calculate_score(len(borrar_filas))

    def ejecutar(self):

        # update
        self.entrada()
        self.timer_update()
        self.sprites.update()

        # drawing
        self.superficie.fill(NEGRO)
        self.sprites.draw(self.superficie)

        # self.draw_grid()
        self.mostrar_superficie.blit(self.superficie, (PADDING, PADDING))
        pygame.draw.rect(self.mostrar_superficie, LINE_COLOR, self.rect, 2, 2)
