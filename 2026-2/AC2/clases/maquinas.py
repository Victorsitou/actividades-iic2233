from clases.fabrica import Caja, CajaRechazadaError
from utils import codigo_valido


class MaquinaInspeccion:
    def __init__(self, peso_maximo: float) -> None:
        self.peso_maximo = peso_maximo

    def inspeccionar(self, caja: Caja) -> None:
        if not codigo_valido(caja.codigo):
            raise CajaRechazadaError("código inválido")

        if caja.nombre == "":
            raise CajaRechazadaError("nombre vacío")

        try:
            peso = float(caja.peso)
        except ValueError:
            raise CajaRechazadaError("peso no númerico")

        if peso <= 0:
            raise CajaRechazadaError("peso menor o igual a cero")

        if peso > self.peso_maximo:
            raise CajaRechazadaError("peso sobre el máximo")
