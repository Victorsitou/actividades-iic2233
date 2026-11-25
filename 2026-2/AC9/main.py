from algoritmos import bfs, dfs
from generador_laberintos import generar_laberinto
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

import time

TAMANOS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
DENSIDAD = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
CANTIDAD_VECES = 5

if __name__ == "__main__":
    # Parte 1
    datos = []
    for tamano in TAMANOS:
        for densidad in DENSIDAD:
            for i in range(CANTIDAD_VECES):
                laberinto = generar_laberinto(tamano, densidad)

                # DFS
                tiempo_inicio_dfs = time.perf_counter()
                camino_dfs = dfs(laberinto.grafo, laberinto.inicio, laberinto.meta)
                tiempo_final_dfs = time.perf_counter()

                tiempo_segundos_dfs = tiempo_final_dfs - tiempo_inicio_dfs
                tiempo_milisegundos_dfs = tiempo_segundos_dfs * 1000
                cantidad_movimientos_dfs = len(camino_dfs) - 1
                datos.append({
                    "tamano": tamano,
                    "densidad": densidad,
                    "algoritmo": "DFS",
                    "tiempo": tiempo_milisegundos_dfs,
                    "largo": cantidad_movimientos_dfs
                })

                # BFS
                tiempo_inicio_bfs = time.perf_counter()
                camino_bfs = bfs(laberinto.grafo, laberinto.inicio, laberinto.meta)
                tiempo_final_bfs = time.perf_counter()

                tiempo_segundos_bfs = tiempo_final_bfs - tiempo_inicio_bfs
                tiempo_milisegundos_bfs = tiempo_segundos_bfs * 1000
                cantidad_movimientos_bfs = len(camino_dfs) - 1
                datos.append({
                    "tamano": tamano,
                    "densidad": densidad,
                    "algoritmo": "BFS",
                    "tiempo": tiempo_milisegundos_bfs,
                    "largo": cantidad_movimientos_bfs
                })

    datos_df = pd.DataFrame(datos)

    # Parte 2

    datos_procesados = datos_df.groupby(["tamano", "densidad", "algoritmo"]).agg(
        tiempo_promedio=("tiempo", "mean"),
        largo_promedio=("largo", "mean")
    ).reset_index()

    # Parte 3

    DENSIDADES_GRAFICOS = [0.5, 0.6, 0.7, 0.8]
    for densidad in DENSIDADES_GRAFICOS:
        datos_filtrados = datos_procesados[datos_procesados["densidad"] == densidad]
        d_filtrados_bfs = datos_filtrados[datos_filtrados["algoritmo"] == "BFS"]
        d_filtrados_dfs = datos_filtrados[datos_filtrados["algoritmo"] == "DFS"]
        plt.figure(figsize=(10, 5))
        plt.scatter(
            d_filtrados_bfs["tamano"],
            d_filtrados_bfs["tiempo_promedio"],
            color="blue",
            label="BFS"
        )
        plt.scatter(
            d_filtrados_dfs["tamano"],
            d_filtrados_dfs["tiempo_promedio"],
            color="red",
            label="DFS"
        )
        plt.title(f"Densidad: {densidad}")
        plt.xlabel("Tamaño")
        plt.ylabel("Tiempo promedio (milisegundos)")
        plt.legend()
        plt.savefig(f"imagenes/densidad_{densidad}.png")
        plt.close()

    TAMANOS_GRAFICOS = [50, 60, 70, 80]
    for tamano in TAMANOS_GRAFICOS:
        datos_filtrados = datos_procesados[datos_procesados["tamano"] == tamano]
        d_filtrados_bfs = datos_filtrados[datos_filtrados["algoritmo"] == "BFS"]
        d_filtrados_dfs = datos_filtrados[datos_filtrados["algoritmo"] == "DFS"]
        plt.figure(figsize=(10, 5))
        plt.scatter(
            d_filtrados_bfs["densidad"],
            d_filtrados_bfs["largo_promedio"],
            color="blue",
            label="BFS"
        )
        plt.scatter(
            d_filtrados_dfs["densidad"],
            d_filtrados_dfs["largo_promedio"],
            color="red",
            label="DFS"
        )
        plt.title(f"Tamaño: {densidad}")
        plt.xlabel("Densidad")
        plt.ylabel("Largo promedio (movimientos)")
        plt.legend()
        plt.savefig(f"imagenes/tamano_{tamano}.png")
        plt.close()

    # Bonus 1
    datos_procesados_dfs = datos_procesados[datos_procesados["algoritmo"] == "DFS"]
    plt.figure()
    ax = plt.axes(projection="3d")
    ax.scatter(
        datos_procesados_dfs["tamano"],
        datos_procesados_dfs["densidad"],
        datos_procesados_dfs["tiempo_promedio"],
        color="green",
        label="Tiempo promedio según tamaño y densidad"
    )
    ax.set_title("Visualización 3D")
    ax.set_xlabel("Tamaño")
    ax.set_ylabel("Densidad")
    ax.set_zlabel("Tiempo promedio (milisegundos)")
    ax.legend()
    plt.savefig("imagenes/grafico_3d.png")
