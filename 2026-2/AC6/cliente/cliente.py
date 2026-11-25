import socket
import sys
import pickle
import time

from cifrado import cifrar_bytes_mensaje, descifrar_bytes_mensaje


class Cliente:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        # Ahora nos conectamos al servidor y nos devuelve el número de cliente
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        data = pickle.loads(self.socket.recv(4096))
        if data["tipo"] != "numero":
            # TODO: mejor manejo o asumir que siempre llega numero
            print("Ha habido un error al conectarse al servidor")
            return
        self.numero = data["numero_cliente"]
        self.terminado = False

        self.jugar()

    def jugar(self):
        while True:
            data = pickle.loads(self.socket.recv(8192))
            print(f"[SERVER] Turno del cliente {data['turno_actual']}")
            if self.numero == data["turno_actual"]:
                print("[CLIENTE] Es tu hora de jugar, elige un número: ")
                num = input()
                while not num.isnumeric():
                    print("[CLIENTE] Elige un numero, no otra cosa")
                num_list = []
                for n in num:
                    num_list.append(int(n))

                self.socket.sendall(pickle.dumps(
                    {
                        "numero_cliente": self.numero,
                        "numeros": num_list
                    }
                ))
            data = pickle.loads(self.socket.recv(8192))
            if data["tipo"] == "mensaje":
                print(data["mensaje"])
            time.sleep(1)

            data = pickle.loads(self.socket.recv(8192))
            if data["tipo"] == "mensaje":
                print(data["mensaje"])

                if "adivinado" in data["mensaje"]:
                    # Ya ha terminado
                    print("[CLIENTE] Juego terminado")
                    self.cerrar_socket()
                    return

            time.sleep(1)


    def cerrar_socket(self):
        self.socket.close()


if __name__ == '__main__':
    # Se recibe el puerto y host por consola:
    # Sintaxis: <comando python> cliente.py <puerto> <host>
    #     P.ej:          python3 cliente.py 4444 localhost
    # Si no llega uno de los valores, entonces se entrega un valor por defecto
    PORT = 23678 if len(sys.argv) < 2 else int(sys.argv[1])
    HOST = 'localhost' if len(sys.argv) < 3 else sys.argv[2]

    cliente = Cliente(HOST, PORT)
    try:
        pass
    except KeyboardInterrupt:
        cliente.cerrar_socket()
