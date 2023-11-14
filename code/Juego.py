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
        self.velocidad_bajada = ACTUALIZAR_VELOCIDAD_INICIO
        self.bajar_aumentar_velocidad = self.velocidad_bajada * 0.3
        self.presionar_abajo = False
        self.temporizadores = {
            'movimiento vertical': Temporizador(self.velocidad_bajada, True, self.movimiento_abajo),
            'movimiento horizontal': Temporizador(TIEMPO_ESPERA_MOVIMIENTO),
            'rotacion': Temporizador(TIEMPO_ESPERA_ROTACION)
        }
        self.temporizadores['movimiento vertical'].activar()

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
            self.velocidad_bajada *= 0.75
            self.bajar_aumentar_velocidad = self.velocidad_bajada * 0.3
            self.temporizadores['vertical move'].duracion = self.velocidad_bajada

        self.actualizar_puntaje(self.current_lines, self.current_score, self.current_level)

    def check_game_over(self):
        for block in self.tetromino.bloques:
            if block.posicion.y < 0:
                exit()

    def crear_nuevo_tetromino(self):
        self.landing_sound.play()
        self.check_game_over()
        self.comprobar_filas_terminadas()
        self.tetromino = Tetromino(
            self.obtener_proxima_forma(),
            self.sprites,
            self.crear_nuevo_tetromino,
            self.data)

    def atualizar_temporizador(self):
        for timer in self.temporizadores.values():
            timer.actualizar()

    def movimiento_abajo(self):
        self.tetromino.mover_hacia_abajo()

    # Entrada de teclado del usuario
    def entrada(self):
        keys = pygame.key.get_pressed()

        # check movimientos horizontales
        if not self.temporizadores['movimiento horizontal'].activo:
            if keys[pygame.K_LEFT]:
                self.tetromino.mover_horizontal(-1)
                self.temporizadores['movimiento horizontal'].activar()
            if keys[pygame.K_RIGHT]:
                self.tetromino.mover_horizontal(1)
                self.temporizadores['movimiento horizontal'].activar()

        # check rotacion
        if not self.temporizadores['rotacion'].activo:
            if keys[pygame.K_UP]:
                self.tetromino.rotar()
                self.temporizadores['rotacion'].activar()

        # aumento de velocidad de bajada
        if not self.presionar_abajo and keys[pygame.K_DOWN]:
            self.presionar_abajo = True
            self.temporizadores['movimiento vertical'].duracion = self.bajar_aumentar_velocidad

        if self.presionar_abajo and not keys[pygame.K_DOWN]:
            self.presionar_abajo = False
            self.temporizadores['movimiento vertical'].duracion = self.velocidad_bajada

    def comprobar_filas_terminadas(self):

        # obtener los índices de fila completos
        borrar_filas = []
        for i, row in enumerate(self.data):
            if all(row):
                borrar_filas.append(i)

        if borrar_filas:
            for borrar_fila in borrar_filas:

                # borrar filas completas
                for block in self.data[borrar_fila]:
                    block.kill()

                # mover bloques hacia abajo
                for row in self.data:
                    for block in row:
                        if block and block.posicion.y < borrar_fila:
                            block.posicion.y += 1

            # reconstruir los datos de campo
            self.data = [[0 for x in range(COLUMNAS)] for y in range(FILAS)]
            for block in self.sprites:
                self.data[int(block.posicion.y)][int(block.posicion.x)] = block

            # actualizar puntuación
            self.calculate_score(len(borrar_filas))

    def ejecutar(self):

        # actualización
        self.entrada()
        self.atualizar_temporizador()
        self.sprites.update()

        # dibujo
        self.superficie.fill(NEGRO)
        self.sprites.draw(self.superficie)

        self.mostrar_superficie.blit(self.superficie, (PADDING, PADDING))
        pygame.draw.rect(self.mostrar_superficie, COLOR_LINEA, self.rect, 2, 2)
