LETRAS_VALIDAS = [
    "B",
    "C",
    "D",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "P",
    "R",
    "S",
    "T",
    "V",
    "W",
    "X",
    "Y",
    "Z"
]
NUMERO_VALIDOS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def generar_rango_letras():
    for letra1 in LETRAS_VALIDAS:
        for letra2 in LETRAS_VALIDAS:
            yield f"{letra1}{letra2}"


def generar_rango_numeros():
    for num1 in NUMERO_VALIDOS:
        for num2 in NUMERO_VALIDOS:
            yield f"{num1}{num2}"


class OficinaEmisora:
    generador_rango1 = generar_rango_letras()

    def __init__(self) -> None:
        try:
            self.rango1 = next(OficinaEmisora.generador_rango1)
        except StopIteration:
            raise ValueError(
                "Se han acabado las combinaciones de patentes posibles"
                " ya no pueden existir más oficinas."
            )
        self.rango2 = generar_rango_letras()
        self.rango3 = generar_rango_numeros()
        self.generador_patentes = self.generar_patentes()

    def generar_patentes(self):
        for valor_rango2 in self.rango2:
            for valor_rango3 in self.rango3:
                yield f"{self.rango1}{valor_rango2}{valor_rango3}"
            self.rango3 = generar_rango_numeros()  # Reiniciamos el generador de numeros

        # Si llegamos acá al final entonces es porque ya agotamos todas las combinaciones
        # Así que pasamos al siguiente rango1
        try:
            self.rango1 = next(OficinaEmisora.generador_rango1)
        except StopIteration:
            raise ValueError(
                "Se han acabado las combinaciones de patentes posibles"
                " ya no pueden existir más patentes."
            )
        self.generador_patentes = self.generar_patentes()
