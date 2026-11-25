from random import choice, randint
from oficina_emisora import OficinaEmisora, generar_rango_letras
from registro_patentes import RegistroPatentes

MARCAS = (
    "Toyota",
    "Kia",
    "Hyundai",
    "Mazda",
    "Nissan",
    "Suzuki",
)

MODELOS = (
    "Yaris",
    "Rio",
    "Accent",
    "3",
    "Sentra",
    "Swift",
)


def simular_nuevo_vehiculo():
    """
    Crea un nuevo vehiculo random
    """
    return (
        randint(0, 49),
        choice(MARCAS),
        choice(MODELOS),
        randint(2007, 2026),
    )

if __name__ == "__main__":
    ### Completar: Inicializar oficinas
    oficinas = []
    for i in range(0, 50):
        oficinas.append(OficinaEmisora())
    
    ### Completar: Inicializar registro
    registro = RegistroPatentes()

    ### Registrar vehiculos
    for _ in range(500):
        numero_oficina, marca, modelo, anho = simular_nuevo_vehiculo()
        registro.anadir_vehiculo(oficinas, numero_oficina, marca, modelo, anho)

        # Completar: Registrar vehiculo

    ### Consultas: Sacar comentario cuando esten implementadas

    print("Vehículos del año 2023:")
    print(list(registro.vehiculos_por_anho(2023)))

    print("Antigüedad de los vehículos en 2026:")
    print(list(registro.antiguedades_registros(2026)))

    print("Marcas por año:")
    print(registro.marcas_por_anho())
