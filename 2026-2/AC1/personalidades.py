from bases import Aldeano, Interaccion
from regalo import Regalo

PRECIO_CARO = 5000


class Cascarrabias(Aldeano):
    """
    Aldeanos a los que solo los impresionan los regalos caros
    """

    def __add__(self, regalo: Regalo) -> Interaccion:
        """
        POR COMPLETAR (Parte 3):
        """
        cambio_puntos = 0
        if regalo.precio >= PRECIO_CARO:
            cambio_puntos = 10
        else:
            cambio_puntos = -5
        self.amistad += cambio_puntos
        return Interaccion(self, regalo, cambio_puntos)


class Alegre(Aldeano):
    """
    Aldeanos que agradecen cualquier regalo, y que se vuelven locos
    con la fruta
    """

    def __add__(self, regalo: Regalo) -> Interaccion:
        """
        POR COMPLETAR (Parte 3)
        """
        cambio_puntos = 0
        if regalo.categoria == "fruta":
            cambio_puntos = 12
        else:
            cambio_puntos = 8
        self.amistad += cambio_puntos
        return Interaccion(self, regalo, cambio_puntos)


class Presumida(Aldeano):
    """
    Aldeanos que solo valoran la ropa, y que ademas exigen que sea cara
    """

    def __add__(self, regalo: Regalo) -> Interaccion:
        """
        POR COMPLETAR (Parte 3)
        """
        cambio_puntos = 0
        if regalo.categoria == "ropa":
            if regalo.precio >= PRECIO_CARO:
                cambio_puntos = 15
            else:
                cambio_puntos = 6
        else:
            cambio_puntos = 1
        self.amistad += cambio_puntos
        return Interaccion(self, regalo, cambio_puntos)
