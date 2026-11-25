from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from oficina_emisora import OficinaEmisora


class RegistroPatentes:
    def __init__(self) -> None:
        self.vehiculos = []

    def anadir_vehiculo(
        self,
        oficinas: list["OficinaEmisora"],
        numero_oficina: int,
        marca: str,
        modelo: str,
        ano: int
    ) -> None:
        if numero_oficina < 0 or numero_oficina > 49:
            raise ValueError("El numero de oficina no está en el rango válido 0-49")
        if ano < 2007 or ano > 2026:
            raise ValueError("El ano no está en el rango válido de 2007-2026")

        oficina_emisora = oficinas[numero_oficina]
        self.vehiculos.append(
            {
                "oficina": numero_oficina,
                "marca": marca,
                "modelo": modelo,
                "año": ano,
                "patente": next(oficina_emisora.generador_patentes)
            }
        )

    def vehiculos_por_anho(self, anho: int):
        return filter(lambda vehiculo: vehiculo["año"] == anho, self.vehiculos)

    def antiguedades_registros(self, anho_actual: int):
        return list(map(lambda vehiculo: anho_actual - vehiculo["año"], self.vehiculos))

    def marcas_por_anho(self):
        anhos = {}
        for vehiculo in self.vehiculos:
            marcas = anhos.get(vehiculo["año"], set())
            marcas.add(vehiculo["marca"])
            anhos[vehiculo["año"]] = marcas
        return anhos
