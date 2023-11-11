from pygame.time import get_ticks


# Define los tiempos de transiciond e los bloques
class Temporizador:
    def __init__(self, duracion, repetido=False, func=None):
        self.repetido = repetido
        self.func = func
        self.duracion = duracion

        self.start_time = 0
        self.active = False

    def activar(self):
        self.active = True
        self.start_time = get_ticks()

    def desactivar(self):
        self.active = False
        self.start_time = 0

# Llama esta funcion cada frame del juego
    def actualizar(self):
        current_time = get_ticks()
        if current_time - self.start_time >= self.duracion and self.active:

            # llamada a funcion
            if self.func and self.start_time != 0:
                self.func()

            # resetear temporizador
            self.desactivar()

            # repetir temporizador
            if self.repetido:
                self.activar()
