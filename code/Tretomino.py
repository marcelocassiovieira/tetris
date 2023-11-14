from Constantes import *
from Bloque import Bloque


class Tetromino:
    def __init__(self, forma, group, crear_nuevo_tetromino, datos_campo):

        # configuracion
        self.forma = forma
        self.posicion_bloques = TETROMINOS[forma]['forma']
        self.color = TETROMINOS[forma]['color']
        self.crear_nuevo_tetromino = crear_nuevo_tetromino
        self.datos_campo = datos_campo

        # create blocks
        self.bloques = [Bloque(group, posicion, self.color) for posicion in self.posicion_bloques]

    # colisiones
    def siguiente_movimiento_colisión_horizontal(self, blocks, amount):
        lista_colision = [bloque.colision_horizontal(int(bloque.posicion.x + amount), self.datos_campo) for bloque in self.bloques]
        return True if any(lista_colision) else False

    def siguiente_movimiento_colision_vertical(self, bloques, monto):
        lista_colision = [bloque.colision_vertical(int(bloque.posicion.y + monto), self.datos_campo) for bloque in self.bloques]
        return True if any(lista_colision) else False

    # movimientos
    def mover_horizontal(self, monto):
        if not self.siguiente_movimiento_colisión_horizontal(self.bloques, monto):
            for bloque in self.bloques:
                bloque.posicion.x += monto

    def mover_hacia_abajo(self):
        if not self.siguiente_movimiento_colision_vertical(self.bloques, 1):
            for bloque in self.bloques:
                bloque.posicion.y += 1
        else:
            for bloque in self.bloques:
                self.datos_campo[int(bloque.posicion.y)][int(bloque.posicion.x)] = bloque
            self.crear_nuevo_tetromino()

    # rotaciones
    def rotar(self):
        if self.forma != 'O':

            # 1. pivot
            pivot_pos = self.bloques[0].posicion

            # 2. nuevas posiciones de bloques
            nuevas_posiciones_bloque = [block.rotar(pivot_pos) for block in self.bloques]

            # 3. chequeo de colisiones
            for pos in nuevas_posiciones_bloque:
                # horizontal
                if pos.x < 0 or pos.x >= COLUMNAS:
                    return

                # control de campo -> colisión con otras piezas
                if self.datos_campo[int(pos.y)][int(pos.x)]:
                    return

                # control vertical / de final - base
                if pos.y > FILAS:
                    return

            # 4. implementar nuevas posiciones
            for i, bloque in enumerate(self.bloques):
                bloque.posicion = nuevas_posiciones_bloque[i]
