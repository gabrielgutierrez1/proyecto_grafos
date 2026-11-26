"""Integración y escenarios de referencia, independientes de la interfaz gráfica."""
from __future__ import annotations

from dataclasses import dataclass

from .camino_minimo import camino_minimo
from .corte_minimo import rutas_y_corte
from .grafo import Arco, GrafoLaberinto, crear_grafo_inicial


@dataclass
class Resultado:
    camino: list[str] | None
    longitud: int | None
    rutas: list[list[str]]
    corte: set[Arco]


def calcular_resultado(grafo: GrafoLaberinto) -> Resultado:
    """Calcula sobre una misma instantánea de los arcos activos."""
    activos = grafo.arcos_activos
    camino, longitud = camino_minimo(grafo.vertices, activos, grafo.entrada, grafo.salida)
    rutas, corte = rutas_y_corte(grafo.vertices, activos, grafo.entrada, grafo.salida)
    return Resultado(camino, longitud, rutas, corte)


def crear_escenarios(entrada: str = "s", salida: str = "t") -> list[tuple[str, GrafoLaberinto]]:
    """Las dos modificaciones parten del original y conservan los extremos."""
    escenarios = []
    for nombre in ("G0 · Original", "G1 · Bloquear H → t", "G2 · Agregar A → t"):
        grafo = crear_grafo_inicial()
        grafo.cambiar_extremos(entrada, salida)
        escenarios.append((nombre, grafo))
    escenarios[1][1].bloquear_arco("H", "t")
    escenarios[2][1].agregar_arco("A", "t")
    return escenarios

