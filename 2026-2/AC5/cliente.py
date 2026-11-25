import requests

PUERTO = "8080"
BASE = f"http://127.0.0.1:{PUERTO}"

if __name__ == "__main__":
    print("Hola, bienvenido al mejor juego del mundo, \"Adivina el número\"")
    nombre = input("Primero que todo, dame tu nombre: ")

    print(f"Ah, hola {nombre}, empecemos...")
    partida = False

    def imprimir_opciones(partida):
        print(f"""
1. Iniciar o continuar partida
{"2. Enviar intento\n0. Salir" if partida else "0. Salir"}
""")
        opcion = input("Elige una opción: ")
        opciones = ["0", "1"]
        if partida:
            opciones.append("2")

        while opcion not in opciones:
            opcion = input("Esa opción es incorrecta, elige nuevamente una opcion: ")

        if opcion == "0":
            print(f"Sayonara {nombre}...")
            quit()
        elif opcion == "1":
            req = requests.post(
                BASE + "/iniciar_partida",
                json={"nombre": nombre}
            )
            if req.status_code != 200:
                print("Ha ocurrido un error al iniciar la partida, intenta nuevamente...")
                imprimir_opciones()
                return

            response = req.json()
            if not response["nueva"]:
                print(
                    "Se ha encontrado una partida no completa, continuando con esa "
                    + f"la cual tiene {response['intentos']} intentos restantes. ")
            else:
                print("Se ha iniciado una nueva partida, buena suerte!")
            partida = True
            imprimir_opciones(partida)
        elif opcion == "2":
            numero = input("Elige tu número para adivinar: ")
            req = requests.post(
                BASE + "/intento",
                json={"nombre": nombre, "numero": numero}
            )
            if req.status_code == 403:
                print("Ya no tienes más intentos, prueba iniciando una nueva partida")
                imprimir_opciones()
                return
            if req.status_code == 400:
                response = req.json()
                print(response["message"])
                imprimir_opciones(partida)
                return
            if req.status_code != 200:
                print("Ha ocurrido un error al enviar el intento, intenta nuevamente...")
                imprimir_opciones(partida)
                return

            response = req.json()
            if "numero" in response:
                # Si está es porque ya terminó la partida
                print(f"La partida ya ha terminado... el número real era {response['numero']}")
                imprimir_opciones(False)
                return
            else:

                if response["success"]:
                    print(
                        "Felicidades, has encontrado el número..." +
                        "me pregunto cómo lo habrás hecho"
                    )
                    imprimir_opciones(False)
                    return
                else:
                    print(response["message"] + f". Te quedan {response['intentos']} intentos")
            imprimir_opciones(partida)

    imprimir_opciones(partida)
