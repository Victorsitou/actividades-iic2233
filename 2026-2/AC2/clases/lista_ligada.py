from __future__ import annotations

from clases.fabrica import Caja, Registro


class Nodo:
    def __init__(self, valor: Caja | Registro) -> None:
        self.valor = valor
        self.siguiente = None

    def __repr__(self) -> str:
        return f"Nodo[{self.valor!r}]"


class ListaLigada:
    def __init__(self) -> None:
        self.cabeza = None
        self.cola = None
        self.largo = 0

    def agregar(self, valor: Caja | Registro) -> None:
        nuevo_nodo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.largo += 1

    def retirar_primera(self) -> Caja | Registro:
        if not self.cabeza:
            raise IndexError("La cinta esta vacía.")

        nodo_retorno = self.cabeza
        if self.largo == 1:
            # Solo tiene la cabeza
            self.cabeza = None
        else:
            # Movemos a la izquierda
            self.cabeza = self.cabeza.siguiente
            if self.cabeza == self.cola:
                # Si la cabeza coincide con la cola entonces es porque ya no existe cola
                self.cola = None
        self.largo -= 1
        return nodo_retorno.valor

    def __len__(self) -> int:
        return self.largo

    def __iter__(self) -> IteradorListaLigada:
        return IteradorListaLigada(self.cabeza)


class IteradorListaLigada:
    def __init__(self, cabeza: Nodo | None) -> None:
        self.cabeza = cabeza

    def __iter__(self) -> IteradorListaLigada:
        return self

    def __next__(self) -> Caja | Registro:
        if not self.cabeza:
            raise StopIteration("Llegamos al final")
        nodo_retornado = self.cabeza
        self.cabeza = self.cabeza.siguiente
        return nodo_retornado.valor
