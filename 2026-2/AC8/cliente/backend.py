import json
import socket

from PyQt6.QtCore import QObject, Qt, QTimer, pyqtSignal, QThread

import parametros as p
from protocolo import enviar, recibir


class EscucharQThread(QThread):
    senal_mensaje = pyqtSignal(dict)
    senal_desconectado = pyqtSignal()

    def __init__(self, socket: socket.socket) -> None:
        super().__init__()
        self.socket = socket

    def run(self) -> None:
        try:
            while True:
                mensaje_bytes = recibir(self.socket)
                self.senal_mensaje.emit(json.loads(mensaje_bytes.decode("utf-8")))
        except (ConnectionError, OSError):
            print("Se perdió la conexión con el servidor")
            self.senal_desconectado.emit()


class Logica(QObject):
    # VentanaInicio
    senal_vi_avisar = pyqtSignal(str)
    senal_vi_habilitar = pyqtSignal(bool)
    senal_vi_cerrar = pyqtSignal()
    # VentanaJuego
    senal_vj_empezar = pyqtSignal(list, str)
    senal_vj_actualizar_estado = pyqtSignal(int, int, int, int)
    senal_vj_actualizar_marcador = pyqtSignal(int, int)
    senal_vj_actualizar_reloj = pyqtSignal(str)
    senal_vj_mensaje_temporal = pyqtSignal(str)
    senal_vj_terminar = pyqtSignal(str)
    # Solo para el bonus
    senal_vj_pausa = pyqtSignal(bool, str)
    senal_vj_aviso_revancha = pyqtSignal(str)
    senal_vj_mostrar_revancha = pyqtSignal()

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread_escuchar = EscucharQThread(self.socket_cliente)

        self.en_ventana_juego = False
        self.y = (p.ALTO_CANCHA - p.ALTO_PALETA) // 2
        self.teclas = set()
        self.segundos_restantes = 0

        self.timer_movimiento = QTimer(self)
        self.timer_movimiento.timeout.connect(self.mover_paleta)
        self.timer_movimiento.setInterval(p.TICK_MOVIMIENTO)
        self.timer_movimiento.start()

        self.timer_reloj = QTimer(self)
        self.timer_reloj.timeout.connect(self.avanzar_reloj)
        self.timer_reloj.setInterval(1000)
        self.timer_reloj.setTimerType(Qt.TimerType.PreciseTimer)
        # Completar: configuración de los timers

    def conectar_a_servidor(self) -> bool:
        try:
            self.socket_cliente.connect((self.host, self.port))
        except ConnectionError:
            print('No me pude conectar al servidor.')
            return False

        self.thread_escuchar.senal_mensaje.connect(self.procesar_mensaje)
        self.thread_escuchar.senal_desconectado.connect(self.manejar_desconexion)
        # TODO: cerrar qobject?
        self.thread_escuchar.start()
        return True

    def enviar_comando(self, mensaje: dict) -> None:
        try:
            enviar(self.socket_cliente, json.dumps(mensaje).encode('utf-8'))
        except (ConnectionError, OSError):
            self.manejar_desconexion()

    def unirse(self, nombre: str) -> None:
        # DONE
        if nombre.strip() == "":
            self.senal_vi_avisar.emit("Debes ingresar un nombre")
            return
        self.enviar_comando({"comando": "unirse", "nombre": nombre})
        self.en_ventana_juego = True

    def procesar_mensaje(self, mensaje: dict) -> None:
        # Completar: procesa un mensaje del servidor
        if mensaje["tipo"] == "aceptado":
            self.senal_vi_avisar.emit("Nombre aceptado, se está esperando un rival.")
        elif mensaje["tipo"] == "rechazado":
            self.senal_vi_avisar.emit("Nombre rechazado: ", mensaje["razon"])
        elif mensaje["tipo"] == "inicio":
            self.empezar_partida(mensaje)
        elif mensaje["tipo"] == "estado":
            self.senal_vj_actualizar_estado.emit(
                mensaje["pelota"][0],
                mensaje["pelota"][1],
                mensaje["paletas"]["izquierda"],
                mensaje["paletas"]["derecha"]
            )
        elif mensaje["tipo"] == "gol":
            self.senal_vj_actualizar_marcador.emit(mensaje["marcador"][0], mensaje["marcador"][1])
            self.senal_vj_mensaje_temporal.emit(f"Gol de {mensaje['goleador']}")
        elif mensaje["tipo"] == "fin":
            self.senal_vj_actualizar_marcador.emit(mensaje["marcador"][0], mensaje["marcador"][1])
            if mensaje["ganador"]:
                self.terminar_partida(f"¡Ha ganado {mensaje['ganador']}!")
            else:
                self.terminar_partida("Ha habido un empate")
        elif mensaje["tipo"] == "rival_desconectado":
            self.terminar_partida("El rival se ha desconectado... saliendo")
        # Bonus: procesa pausa y revancha, y ofrece la revancha al terminar
        pass

    def empezar_partida(self, mensaje: dict) -> None:
        # Completar: prepara la partida y cambia de ventana
        print("Va a empezar la partida!")
        self.senal_vi_cerrar.emit()
        self.segundos_restantes = mensaje["duracion"]
        self.senal_vj_empezar.emit(mensaje["nombres"], self.texto_reloj())

        self.timer_reloj.start()

        # Bonus: reinicia el estado de la paleta
        pass

    def terminar_partida(self, texto: str) -> None:
        self.timer_movimiento.stop()
        self.timer_reloj.stop()
        self.senal_vj_terminar.emit(texto)
        self.cerrar()

    def pedir_pausa(self) -> None:
        # Solo para el bonus
        self.enviar_comando({'comando': 'pausa'})

    def pedir_revancha(self) -> None:
        # Solo para el bonus
        self.enviar_comando({'comando': 'revancha'})

    def cambiar_pausa(self, activa: bool, nombre: str) -> None:
        # Bonus: pausa o reanuda la partida
        pass

    def manejar_desconexion(self) -> None:
        if self.en_ventana_juego:
            self.terminar_partida('Se perdió la conexión con el servidor')
        else:
            self.senal_vi_avisar.emit('Se perdió la conexión con el servidor')
            self.senal_vi_habilitar.emit(False)

    def actualizar_tecla(self, direccion: int, presionada: bool) -> None:
        if presionada:
            self.teclas.add(direccion)
        else:
            self.teclas.discard(direccion)

    def mover_paleta(self) -> None:
        if len(self.teclas) == 0:
            return

        movimiento = self.teclas.pop()
        if movimiento == -1:
            # Va subiendo
            self.y = max(0, self.y-p.VELOCIDAD_PALETA) 
        else:
            # Va bajando
            self.y = min(p.ALTO_CANCHA-p.ALTO_PALETA, self.y+p.VELOCIDAD_PALETA)
        self.enviar_comando({"comando": "mover", "y": self.y})
        pass

    def avanzar_reloj(self) -> None:
        if self.segundos_restantes > 0:
            self.segundos_restantes -= 1
        self.senal_vj_actualizar_reloj.emit(self.texto_reloj())

    def texto_reloj(self) -> str:
        minutos, segundos = divmod(self.segundos_restantes, 60)
        return f'{minutos:02d}:{segundos:02d}'

    def cerrar(self) -> None:
        self.timer_movimiento.stop()
        self.timer_reloj.stop()
        # shutdown despierta al recv que está bloqueado en el otro thread
        try:
            self.socket_cliente.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.socket_cliente.close()
        if self.thread_escuchar is not None:
            self.thread_escuchar.wait()
