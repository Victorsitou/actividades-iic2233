from utilidades import imprimir_reporte
from clases import Cocina
from parametros import NUM_COCINEROS, PEDIDOS_POR_COCINERO, DURACION_SERVICIO


if __name__ == "__main__":
    # COMPLETAR Parte 3: instancia la Cocina y guárdala en la variable "cocina".
    # Luego, simula el servicio y guarda lo que retorna en "resultado".
    cocina = Cocina(
        num_cocineros=NUM_COCINEROS,
        pedidos_por_cocinero=PEDIDOS_POR_COCINERO,
        duracion_servicio=DURACION_SERVICIO
    )
    resultado = cocina.simular_servicio()

    if resultado is None:
        print("\nsimular_servicio() no retornó nada: debe retornar la tupla "
              "(tiempos, no_entregados).")
    else:
        tiempos, no_entregados = resultado
        imprimir_reporte(cocina.pedidos, tiempos, no_entregados)
