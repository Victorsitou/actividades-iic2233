from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QLineEdit, QVBoxLayout
from PyQt6.QtCore import pyqtSignal


class BotonConLabel(QHBoxLayout):
    def __init__(self, texto: str, on_change, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        label = QLabel(f"{texto}: ")
        campo = QLineEdit("")
        campo.textChanged.connect(lambda _: on_change(texto))

        self.addStretch(1)
        self.addWidget(label)
        self.addWidget(campo)
        self.addStretch(1)


class VentanaInicio(QWidget):
    senal_abrir_juego = pyqtSignal(str, str)
    senal_campo_escrito = pyqtSignal(str, str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.show()
        self.listo = False

    def actualizar_alerta(self, texto: str):
        self.label_alerta.setText(texto)

    def juego_listo(self, nombre_j1, nombre_j2):
        self.nombre_j1 = nombre_j1
        self.nombre_j2 = nombre_j2
        self.listo = True

    def init_gui(self):
        self.setGeometry(200, 200, 120, 120)

        contenedor = QVBoxLayout()
        contenedor.addLayout(BotonConLabel("Nombre J1", self.campo_escrito))
        contenedor.addLayout(BotonConLabel("Nombre J2", self.campo_escrito))

        boton_jugar = QPushButton("Jugar", self)
        boton_jugar.resize(boton_jugar.sizeHint())
        boton_jugar.clicked.connect(self.empezar_juego)
        contenedor.addWidget(boton_jugar)

        self.label_alerta = QLabel("Faltan los nombres de dos jugadores.\n\
            No se puede empezar el juego")
        self.label_alerta.resize(self.label_alerta.sizeHint())
        contenedor.addWidget(self.label_alerta)

        self.setLayout(contenedor)

    def campo_escrito(self, texto_label: str):
        texto_campo = self.sender().text()
        self.senal_campo_escrito.emit(texto_campo, texto_label)

    def empezar_juego(self):
        if self.listo:
            self.hide()
            self.senal_abrir_juego.emit(self.nombre_j1, self.nombre_j2)
