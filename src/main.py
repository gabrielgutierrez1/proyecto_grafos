"""Inicio de la interfaz o verificación reproducible desde consola."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

# Al ejecutar el archivo directamente, Python no conoce el paquete src.
# Resolver desde __file__ permite iniciarlo desde cualquier directorio.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

from .camino_minimo import formatear_resultado_camino
from .grafo import crear_grafo_manual


def resumen_consola() -> None:
    from .escenarios import calcular_resultado, crear_escenarios

    escenarios = crear_escenarios() + [("Gm · Caso manual", crear_grafo_manual())]
    for nombre, grafo in escenarios:
        resultado = calcular_resultado(grafo)
        print(f"{nombre}: {formatear_resultado_camino(resultado.camino, resultado.longitud)}")
        print(f"  Rutas independientes: {len(resultado.rutas)}; corte: {sorted(resultado.corte)}")
        for i, ruta in enumerate(resultado.rutas, 1):
            print(f"  R{i}: {' -> '.join(ruta)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulador de laberintos dirigidos")
    parser.add_argument("--consola", action="store_true", help="verificar escenarios sin abrir una ventana")
    args = parser.parse_args()
    if args.consola:
        resumen_consola()
        return
    try:
        from .interfaz import iniciar_interfaz
    except ModuleNotFoundError as error:
        if error.name != "tkinter":
            raise
        parser.exit(1, "Falta Tkinter. En Debian/Ubuntu instala python3-tk.\n")
    from tkinter import TclError
    try:
        iniciar_interfaz()
    except TclError as error:
        parser.exit(1, f"No se pudo iniciar la interfaz: {error}\nEjecuta en una sesión gráfica o usa --consola.\n")


if __name__ == "__main__":
    main()
