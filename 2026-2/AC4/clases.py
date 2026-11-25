from collections import deque
from datetime import datetime, timedelta
from eventos_random import (
    random_tiempo_picado,
    random_tiempo_coccion,
    random_tiempo_emplatado,
    random_se_quema_plato,
    random_tiempo_extra
)
import threading
import time

from parametros import (
    DURACION_SERVICIO,
    MENU,
    NOMBRES_COCINEROS,
    NUM_COCINEROS,
    PEDIDOS_POR_COCINERO,
)
from utilidades import log, iniciar_cronometro
from typing import Deque


class Pedido:
    """
    Un pedido de un cliente. NO MODIFICAR.
    """

    def __init__(self, id_pedido: int, plato: str) -> None:
        self.id_pedido = id_pedido
        self.plato = plato
        self.inicio = None
        self.entrega = None

    def __repr__(self) -> str:
        return f"Pedido #{self.id_pedido} ({self.plato})"


class Cocinero:
    """
    Un cocinero del restaurante. Atiende, de uno en uno, los pedidos que
    tiene asignados en su propia cola.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.pedidos: Deque[Pedido] = deque()
        self.thread = threading.Thread(name=self.nombre, target=self.preparar_pedidos)

    def asignar_pedido(self, pedido: Pedido) -> None:
        """Agrega un pedido al final de su cola. NO MODIFICAR."""
        self.pedidos.append(pedido)

    def preparar_pedidos(self) -> None:
        Cocina.cocina_abierta.wait()
        cocina_cerrada = False
        while self.pedidos:
            pedido = self.pedidos.popleft()
            pedido.inicio = datetime.now()
            log(self.nombre, f"Estoy empezando el pedido {pedido}")

            # picar INDEPENDIENTE
            tiempo_picar = random_tiempo_picado()
            log(self.nombre, f"Estoy empezando a picar los ingredientes para el pedido {pedido}")
            time.sleep(tiempo_picar)

            # cocinar DEPENDIENTE
            Cocina.estufa_ocupada.acquire()
            log(self.nombre, "Estoy usando la estufa ahora!")

            tiempo_coccion = random_tiempo_coccion()
            log(self.nombre, f"Estoy empezando a cocinar el pedido {pedido}")
            time.sleep(tiempo_coccion)
            se_quema = random_se_quema_plato()
            if se_quema:
                log(self.nombre, f"El pedido {pedido} se me ha quemado :(, lo volveré a hacer")
                time.sleep(random_tiempo_extra())

            log(self.nombre, "Ya terminé de usar la estufa")
            Cocina.estufa_ocupada.release()

            # emplatar INDEPENDIENTE
            tiempo_emplatar = random_tiempo_emplatado()
            log(self.nombre, f"Estoy empezando a emplatar el pedido {pedido}")
            time.sleep(tiempo_emplatar)

            pedido.entrega = datetime.now()

            # Hacemos esto para asegurarnos que no haya race condition
            Cocina.registrando_pedido.acquire()
            log(self.nombre, f"Ya entregué el pedido {pedido}")
            Cocina.pedidos_entregados[pedido.id_pedido] = pedido.entrega-pedido.inicio
            Cocina.registrando_pedido.release()

            # Si la cocina ya cerró entonces terminamos.
            if not Cocina.cocina_abierta.is_set():
                cocina_cerrada = True
                break

        # Usamos el lock para asegurarnos que no haya race condition
        Cocina.registrando_pedido.acquire()

        msg = ""
        if cocina_cerrada:
            msg += "La cocina ha cerrado..."
        else:
            msg += "Me he quedado sin pedidos..."
        pendientes = len(self.pedidos)
        if cocina_cerrada and pendientes > 0:
            msg += f" y me han quedado {pendientes} pedidos pendientes"
        elif cocina_cerrada and pendientes < 0:
            msg += " pero no me han quedado pedidos pendientes!"
        log(self.nombre, msg)

        while self.pedidos:
            Cocina.pedidos_pendientes.append(self.pedidos.popleft())
        Cocina.registrando_pedido.release()


class Cocina:
    """
    Un servicio completo del restaurante, de la apertura al cierre.
    """
    cocina_abierta = threading.Event()
    estufa_ocupada = threading.Lock()

    pedidos_entregados = {}
    registrando_pedido = threading.Lock()
    pedidos_pendientes = []

    # COMPLETAR: la estufa no alcanza para dos, y el registro de entregas
    # lo escriben todos los cocineros. Define aquí lo necesario para que
    # solo un cocinero a la vez pueda acceder a cada uno.

    def __init__(self, num_cocineros: int = NUM_COCINEROS,
                 pedidos_por_cocinero: int = PEDIDOS_POR_COCINERO,
                 duracion_servicio: float = DURACION_SERVICIO) -> None:
        self.duracion_servicio = duracion_servicio

        # COMPLETAR: los cocineros no deben empezar a trabajar antes de que
        # abra el restaurante, y deben saber cuándo la cocina cerró

        self.cocineros: dict[str, Cocinero] = self.contratar_cocineros(num_cocineros)
        self.pedidos = self.recibir_pedidos(
            num_cocineros * pedidos_por_cocinero
        )
        self.repartir_pedidos()

    def contratar_cocineros(self, cantidad: int) -> dict[str, Cocinero]:
        """Crea los cocineros del turno. NO MODIFICAR."""
        cocineros: dict[str, Cocinero] = dict()
        for i in range(cantidad):
            nombre = NOMBRES_COCINEROS[i % len(NOMBRES_COCINEROS)]
            cocineros[nombre] = Cocinero(nombre)
        return cocineros

    def recibir_pedidos(self, cantidad: int) -> list[Pedido]:
        """Crea los pedidos de la noche. NO MODIFICAR."""
        return [
            Pedido(i + 1, MENU[i % len(MENU)]) for i in range(cantidad)
        ]

    def repartir_pedidos(self) -> None:
        """Reparte los pedidos entre los cocineros. NO MODIFICAR."""
        cocineros = list(self.cocineros.values())
        for i, pedido in enumerate(self.pedidos):
            cocineros[i % len(cocineros)].asignar_pedido(pedido)

    def cerrar_cocina(self) -> None:
        """Cierra la cocina para nuevos pedidos"""
        log("COCINA", "*** SE CIERRA LA COCINA: no se toman más pedidos ***")
        self.cocina_abierta.clear()

    def simular_servicio(self) -> tuple[dict[int, timedelta], list[Pedido]]:
        # COMPLETAR Parte 2
        for cocinero in list(self.cocineros.values()):
            cocinero.thread.start()

        iniciar_cronometro()
        log("COCINA", "La cocina se ha abierto!")
        self.cocina_abierta.set()

        while self.duracion_servicio > 0:
            self.duracion_servicio -= 1
            time.sleep(1)
        self.cerrar_cocina()

        for cocinero in list(self.cocineros.values()):
            cocinero.thread.join()

        return (self.pedidos_entregados, self.pedidos_pendientes)
