from Constantes import *
from Bloque import Bloque


class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):

        # setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['forma']
        self.color = TETROMINOS[shape]['color']
        self.crear_nuevo_tetromino = create_new_tetromino
        self.field_data = field_data

        # create blocks
        self.blocks = [Bloque(group, posicion, self.color) for posicion in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.colision_horizontal(int(block.posicion.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.colision_vertical(int(block.posicion.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    # movement
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.posicion.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.posicion.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.posicion.y)][int(block.posicion.x)] = block
            self.crear_nuevo_tetromino()

    # rotate
    def rotate(self):
        if self.shape != 'O':

            # 1. pivot point
            pivot_pos = self.blocks[0].posicion

            # 2. new block positions
            new_block_positions = [block.rotar(pivot_pos) for block in self.blocks]

            # 3. collision check
            for pos in new_block_positions:
                # horizontal
                if pos.x < 0 or pos.x >= COLUMNAS:
                    return

                # field check -> collision with other pieces
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return

                # vertical / floor check
                if pos.y > FILAS:
                    return

            # 4. implement new positions
            for i, block in enumerate(self.blocks):
                block.posicion = new_block_positions[i]
