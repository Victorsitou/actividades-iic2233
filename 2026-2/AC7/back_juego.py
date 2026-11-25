from PyQt6.QtCore import QObject, pyqtSignal
from utils import comprobar_ganador_lista_de_listas


class BackendJuego(QObject):
    senal_actualizar_alerta = pyqtSignal(str)
    senal_actualizar_boton = pyqtSignal(int, int, str)
    senal_ganador = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rondas = 0
        self.tablero = [["" for i in range(3)] for i in range(3)]
        self.juego_terminado = False

    def handle_boton_click(self, texto: str, x: int, y: int):
        if self.juego_terminado:
            return

        jugador = self.rondas % 2

        # Primero verificamos que ese botón no esté ya clickeado
        if texto != "":
            self.senal_actualizar_alerta.emit("Posicion ocupada. Elige otra.")
            return

        if jugador == 0:
            # Juega el jugador 1
            self.senal_actualizar_boton.emit(x, y, "O")
            self.tablero[y][x] = "O"
        else:
            # Juega el jugador 2
            self.senal_actualizar_boton.emit(x, y, "X")
            self.tablero[y][x] = "X"

        hay_ganador, ganador = comprobar_ganador_lista_de_listas(self.tablero)
        if hay_ganador:
            self.senal_ganador.emit(ganador)
            self.juego_terminado = True

        self.rondas += 1
