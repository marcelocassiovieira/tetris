from Constantes import *
from random import choice
from sys import exit
from os.path import join
from Tretomino import Tetromino
from Timer import Timer


class Game:
    def __init__(self, get_next_shape, update_score):

        # general
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)

        # timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(self.down_speed, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

        # sound
        self.landing_sound = pygame.mixer.Sound(join('..', 'sounds', 'landing.wav'))
        self.landing_sound.set_volume(0.1)

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.down_speed_faster = self.down_speed * 0.3
            self.timers['vertical move'].duration = self.down_speed

        self.update_score(self.current_lines, self.current_score, self.current_level)

    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                exit()

    def create_new_tetromino(self):
        self.landing_sound.play()
        self.check_game_over()
        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):

        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y))

        self.surface.blit(self.line_surface, (0, 0))

    def input(self):
        keys = pygame.key.get_pressed()

        # checking horizontal movement
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        # check for rotation
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

        # down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed

    def check_finished_rows(self):

        # get the full row indexes
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:

                # delete full rows
                for block in self.field_data[delete_row]:
                    block.kill()

                # move down blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            # rebuild the field data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            # update score
            self.calculate_score(len(delete_rows))

    def run(self):

        # update
        self.input()
        self.timer_update()
        self.sprites.update()

        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
