import socket
import sys
import json
import pickle
import time

from cifrado import cifrar_bytes_mensaje, descifrar_bytes_mensaje
from juego import JuegoOrdenarNumeros


class Servidor:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.juego = JuegoOrdenarNumeros()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes: list[socket.socket] = []
        self.rondas = 0
        self.terminado = False

    @property
    def turno_actual(self):
        return self.rondas % len(self.clientes)

    def iniciar_juego(self):
        while not self.terminado:
            self.terminado = self.avisar_jugadores()
            self.rondas += 1
            time.sleep(1)

    def bind_listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(3)
        while len(self.clientes) < 3:
            socket_cliente, direccion = self.socket.accept()
            print(f"Recibido un cliente con dirección: {direccion}")
            socket_cliente.sendall(pickle.dumps({"tipo": "numero", "numero_cliente": len(self.clientes)}))
            self.clientes.append(socket_cliente)

        self.iniciar_juego()

    def enviar_mensaje_a_todos(self, mensaje: bytes):
        for i, cliente in enumerate(self.clientes):
            try:
                cliente.sendall(mensaje)
            except socket.error:
                print(f"Ha habido un error al enviarle un mensaje al cliente {i}")

    def avisar_jugadores(self):
        print("[SERVER] Enviar mensaje de turno a todos.")
        self.enviar_mensaje_a_todos(pickle.dumps({"tipo": "turno", "turno_actual": self.turno_actual}))

        socket_respuesta = self.clientes[self.turno_actual]
        respuesta_jugador_bytes = socket_respuesta.recv(4096)
        respuesta_jugador = pickle.loads(respuesta_jugador_bytes)
        aciertos = self.juego.comprobar_elementos(respuesta_jugador["numeros"])

        self.enviar_mensaje_a_todos(
            pickle.dumps(
                {
                    "tipo": "mensaje",
                    "mensaje": f"Acertó {aciertos} de {self.juego.cantidad_elementos}"
                }
            )
        )

        if aciertos == self.juego.cantidad_elementos:
            self.enviar_mensaje_a_todos(
                pickle.dumps(
                    {
                        "tipo": "mensaje",
                        "mensaje": f"El jugador {self.turno_actual} ha adivinado todos los números."                     
                    }
                )
            )
            self.cerrar_sockets()
            return True
        else:
            self.enviar_mensaje_a_todos(
                pickle.dumps(
                    {
                        "tipo": "mensaje",
                        "mensaje": "El juego continua"
                    }
                )
            )
            return False

    def cerrar_sockets(self):
        for cliente in self.clientes:
            cliente.close()


if __name__ == '__main__':
    # Se recibe el puerto y host por consola:
    # Sintaxis: <comando python> servidor.py <puerto> <host>
    #     P.ej:          python3 servidor.py 4444 localhost
    # Si no llega uno de los valores, entonces se entrega un valor por defecto
    PORT = 23678 if len(sys.argv) < 2 else int(sys.argv[1])
    HOST = 'localhost' if len(sys.argv) < 3 else sys.argv[2]

    servidor = Servidor(HOST, PORT)
    servidor.bind_listen()

    try:
        pass
    except (KeyboardInterrupt, BrokenPipeError):
        pass
    finally:
        servidor.cerrar_sockets()

    exit(1)
