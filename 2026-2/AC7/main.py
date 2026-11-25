import sys
from PyQt6.QtWidgets import QApplication

from front_juego import VentanaJuego
from back_juego import BackendJuego

from front_inicio import VentanaInicio
from back_inicio import BackendInicio


if __name__ == '__main__':
    def hook(type_, value, traceback) -> None:
        # Imprimimos el error con el hook original de Python. Al instalar
        # nuestro propio sys.excepthook, PyQt no cierra el programa
        sys.__excepthook__(type_, value, traceback)

    sys.excepthook = hook

    app = QApplication([])

    # Inicio
    ventana_inicio = VentanaInicio()
    back_inicio = BackendInicio()
    ventana_inicio.senal_campo_escrito.connect(back_inicio.handle_campo_escrito)
    back_inicio.senal_actualizar_alerta.connect(ventana_inicio.actualizar_alerta)
    back_inicio.senal_juego_listo.connect(ventana_inicio.juego_listo)

    # Juego
    ventana_juego = VentanaJuego()
    back_juego = BackendJuego()
    ventana_juego.senal_boton_click.connect(back_juego.handle_boton_click)
    back_juego.senal_actualizar_alerta.connect(ventana_juego.actualizar_alerta)
    back_juego.senal_actualizar_boton.connect(ventana_juego.actualizar_boton)
    back_juego.senal_ganador.connect(ventana_juego.actualizar_ganador)

    ventana_inicio.senal_abrir_juego.connect(ventana_juego.mostrar_ventana)
    sys.exit(app.exec())
