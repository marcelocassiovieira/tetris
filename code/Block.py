from Constantes import *


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):

        # general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):

        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True

        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True

        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):

        self.rect.topleft = self.pos * CELL_SIZE