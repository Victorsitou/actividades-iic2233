from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtCore import pyqtSignal


class VentanaJuego(QWidget):
    senal_boton_click = pyqtSignal(str, int, int)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rondas = 0
        self.tablero = [["" for i in range(3)] for i in range(3)]
        self.juego_terminado = False

    def mostrar_ventana(self, nombre_j1: str, nombre_j2: str):
        self.nombre_j1 = nombre_j1
        self.nombre_j2 = nombre_j2
        self.init_gui()
        self.show()

    def actualizar_alerta(self, texto: str):
        self.label_alerta.setText(texto)

    def actualizar_boton(self, x: int, y: int, texto: str):
        boton = self.grilla.itemAtPosition(x, y).widget()
        boton.setText(texto)

    def actualizar_ganador(self, ganador: str):
        if ganador == "O":
            self.label_alerta.setText(f"Felicidades, ha ganado O: {self.nombre_j1}")
        else:
            self.label_alerta.setText(f"Felicidades, ha ganado X: {self.nombre_j2}")

    def init_gui(self):
        contenedor_principal = QVBoxLayout()

        self.grilla = QGridLayout()
        posiciones = [(i, j) for i in range(3) for j in range(3)]
        for i in range(len(posiciones)):
            posicion = posiciones[i]
            boton = QPushButton("")
            boton.resize(boton.sizeHint())
            boton.clicked.connect(self.handle_boton_click)
            self.grilla.addWidget(boton, *posicion)

        contenedor_principal.addLayout(self.grilla)

        contenedor_jugadores = QHBoxLayout()
        contenedor_jugadores.addWidget(QLabel(f"J1 (O): {self.nombre_j1}"))
        contenedor_jugadores.addWidget(QLabel(f"J2 (X): {self.nombre_j2}"))
        contenedor_principal.addLayout(contenedor_jugadores)

        self.label_alerta = QLabel("Ha empezado el juego!")
        contenedor_principal.addWidget(self.label_alerta)

        self.setLayout(contenedor_principal)

    def handle_boton_click(self):
        boton = self.sender()
        indice = self.grilla.indexOf(boton)
        posicion = self.grilla.getItemPosition(indice)
        self.senal_boton_click.emit(boton.text(), posicion[0], posicion[1])
