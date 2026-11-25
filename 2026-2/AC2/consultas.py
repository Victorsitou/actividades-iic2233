from collections.abc import Iterator

from clases.fabrica import Registro
from clases.lista_ligada import ListaLigada


def registros_por_resultado(
    bitacora: ListaLigada,
    resultado: str,
) -> Iterator[Registro]:
    return (registro for registro in bitacora if registro.resultado == resultado)


def generar_reporte(
    bitacora: ListaLigada,
    resultado: str,
) -> Iterator[str]:
    return (
        f"{registro.codigo}: {registro.detalle}"
        for registro in registros_por_resultado(bitacora, resultado)
    )
