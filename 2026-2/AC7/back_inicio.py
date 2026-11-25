from PyQt6.QtCore import pyqtSignal, QObject


class BackendInicio(QObject):
    senal_actualizar_alerta = pyqtSignal(str)
    senal_juego_listo = pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre_j1 = None
        self.nombre_j2 = None

    def handle_campo_escrito(self, texto_campo: str, texto_label: str):
        if texto_label == "Nombre J1":
            self.nombre_j1 = texto_campo
        else:
            self.nombre_j2 = texto_campo

        if self.nombre_j1 and not self.nombre_j2:
            self.senal_actualizar_alerta.emit("Falta el nombre de un jugador\n\
                No se puede empezar el juego")
        elif self.nombre_j2 and not self.nombre_j1:
            self.senal_actualizar_alerta.emit("Falta el nombre de un jugador\n\
                No se puede empezar el juego")
        elif not self.nombre_j1 and not self.nombre_j2:
            self.senal_actualizar_alerta.emit("Falta el nombre de dos jugadores\n\
                No se puede empezar el juego")
        elif self.nombre_j1 and self.nombre_j2:
            self.senal_juego_listo.emit(self.nombre_j1, self.nombre_j2)
            self.senal_actualizar_alerta.emit("Ya están los nombres de los jugadores\n\
                Se puede empezar el juego")
