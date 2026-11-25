import json
from flask import Flask, request as req
from pathlib import Path
from random import randrange


app = Flask("servidor")


def buscar_partida(nombre: str, *, con_numero: bool = False):
    """Busca la partida de ese usuario, si no lo encuentra entonces lo crea."""
    dir = Path("partidas")
    for file in dir.iterdir():
        if file.is_file() and file.name == f"{nombre}.json":
            data = json.load(file.open("r", encoding="UTF-8"))

            if not con_numero:
                data.pop("numero")
            data["nueva"] = False

            return data

    # si llegó acá es porque no existe partida
    archivo = dir / f"{nombre}.json"
    data = {"nombre": nombre, "numero": randrange(1, 101), "intentos": 5}
    with archivo.open("w", encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

    if not con_numero:
        data.pop("numero")
    data["nueva"] = True

    return data


@app.route("/iniciar_partida", methods=["POST"])
def iniciar_partida():
    body: dict = req.get_json()

    if not isinstance(body, dict):
        return {"error": "el body tiene que ser un JSON"}, 400
    if not {"nombre"} <= body.keys():
        return {"error": "el body debe contener el nombre del jugador"}, 400

    return buscar_partida(body["nombre"])


@app.route("/intento", methods=["POST"])
def intento():
    body: dict = req.get_json()

    if not isinstance(body, dict):
        return {"error": "el body tiene que ser un JSON"}, 400
    if not {"nombre", "numero"} <= body.keys():
        return {"error": "el body tiene que contener el nombre y el numero"}, 400

    if not body["numero"].isnumeric() or int(body["numero"]) > 100 or int(body["numero"]) < 1:
        return {"message": "El número no es válido, tiene que ser un entero entre 1 y 101"}, 400

    partida = buscar_partida(body["nombre"], con_numero=True)
    if not partida:
        return {"error": "no se ha encontrado una partida con ese nombre"}, 400

    if partida["intentos"] == 0:
        return {"error": "no tienes intentos disponibles"}, 403
    else:
        numero_body = int(body["numero"])
        numero_partida = partida["numero"]

        archivo = Path("partidas") / f"{body['nombre']}.json"
        partida["intentos"] -= 1
        json.dump(partida, archivo.open("w", encoding="UTF-8"))

        response = None
        if numero_body == numero_partida:
            response = {
                "message": "Has encontrado el número!",
                "success": True,
                "intentos": partida["intentos"]
            }
        elif numero_body > numero_partida:
            response = {
                "message": "Prueba con un número menor",
                "success": False,
                "intentos": partida["intentos"]
            }
        elif numero_body < numero_partida:
            response = {
                "message": "Prueba con un número mayor",
                "success": False,
                "intentos": partida["intentos"]
            }

        if partida["intentos"] == 0:
            response["numero"] = numero_partida
            # Como ya no le quedan intentos, borramos el archivo con la partida
            archivo.unlink()
        return response
    return partida


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
