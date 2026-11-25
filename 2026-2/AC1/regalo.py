PRECIO_MAXIMO = 500000


class Regalo:
    """
    Clase que modela un objeto que se le puede regalar a un aldeano
    """

    def __init__(self, nombre: str, categoria: str, precio: int) -> None:
        """
        POR COMPLETAR (Parte 1.1):
        """
        self.nombre = nombre
        self.categoria = categoria
        self._precio = precio

    def __str__(self) -> str:
        return f"{self.nombre}: ({self.precio})"

    def __repr__(self) -> str:
        return f"Regalo(nombre='{self.nombre}', categoria='{self.categoria}', precio={self.precio})"

    @property
    def precio(self) -> int:
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio: int) -> None:
        if nuevo_precio < 0 or nuevo_precio > PRECIO_MAXIMO or not isinstance(nuevo_precio, int):
            print(f"[Aviso] {nuevo_precio} no es un precio válido (0 a {PRECIO_MAXIMO}).")
            print(f"Se mantiene {self.precio}")
            return
        self._precio = nuevo_precio
