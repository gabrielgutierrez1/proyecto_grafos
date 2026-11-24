from __future__ import annotations

from typing import Iterable

from .grafo import Arco


def rutas_independientes(
    vertices: Iterable[str],
    arcos_activos: Iterable[Arco],
    s: str,
    t: str,
) -> list[list[str]]:
    raise NotImplementedError(
        "Pendiente de implementar por Integrante 2 (flujo máximo de capacidad unitaria)."
    )


def rutas_y_corte(
    vertices: Iterable[str],
    arcos_activos: Iterable[Arco],
    s: str,
    t: str,
) -> tuple[list[list[str]], set[Arco]]:
    raise NotImplementedError(
        "Pendiente de implementar por Integrante 2 (Edmonds-Karp + corte mínimo)."
    )
