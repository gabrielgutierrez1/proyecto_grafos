"""Integración y escenarios de referencia, independientes de la interfaz gráfica."""
from __future__ import annotations

from dataclasses import dataclass

from .camino_minimo import camino_minimo
from .corte_minimo import rutas_y_corte
from .grafo import Arco, GrafoLaberinto, crear_grafo_inicial


@dataclass
class Resultado:
    """Agrupa los indicadores calculados sobre una configuración del laberinto."""

    camino: list[str] | None
    longitud: int | None
    rutas: list[list[str]]
    corte: set[Arco]


def calcular_resultado(grafo: GrafoLaberinto) -> Resultado:
    """Ejecuta BFS, rutas disjuntas y corte mínimo sobre una misma instantánea activa.

    Args:
        grafo: Instancia `GrafoLaberinto` con los vértices, arcos activos y extremos.

    Returns:
        Resultado: Objeto con `camino`, `longitud`, `rutas` independientes y `corte` mínimo.
    """
    activos = grafo.arcos_activos
    camino, longitud = camino_minimo(grafo.vertices, activos, grafo.entrada, grafo.salida)
    rutas, corte = rutas_y_corte(grafo.vertices, activos, grafo.entrada, grafo.salida)
    return Resultado(camino, longitud, rutas, corte)


def crear_escenarios(entrada: str = "s", salida: str = "t") -> list[tuple[str, GrafoLaberinto]]:
    """Construye por separado las tres configuraciones comparativas (G0, G1 y G2).

    Args:
        entrada: Vértice de entrada común para la comparación (`'s'` por defecto).
        salida: Vértice de salida común para la comparación (`'t'` por defecto).

    Returns:
        list[tuple[str, GrafoLaberinto]]: Lista de pares `(nombre_escenario, grafo)`
            con G0 original, G1 bloqueando `(H, t)` y G2 agregando `(A, t)`.
    """
    escenarios = []
    for nombre in ("G0 · Original", "G1 · Bloquear H → t", "G2 · Agregar A → t"):
        grafo = crear_grafo_inicial()
        grafo.cambiar_extremos(entrada, salida)
        escenarios.append((nombre, grafo))
    escenarios[1][1].bloquear_arco("H", "t")
    escenarios[2][1].agregar_arco("A", "t")
    return escenarios
