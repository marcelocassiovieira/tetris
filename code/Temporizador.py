from pygame.time import get_ticks


# Define los tiempos de transicion de los bloques
class Temporizador:
    def __init__(self, duracion, repetido=False, func=None):
        self.repetido = repetido
        self.func = func
        self.duracion = duracion

        self.tiempo_inicio = 0
        self.activo = False

    def activar(self):
        self.activo = True
        self.tiempo_inicio = get_ticks()

    def desactivar(self):
        self.activo = False
        self.tiempo_inicio = 0

# Llama esta funcion cada frame del juego
    def actualizar(self):
        tiempo_actual = get_ticks()
        if tiempo_actual - self.tiempo_inicio >= self.duracion and self.activo:

            # llamada a funcion
            if self.func and self.tiempo_inicio != 0:
                self.func()

            # resetear temporizador
            self.desactivar()

            # repetir temporizador
            if self.repetido:
                self.activar()
