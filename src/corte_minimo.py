from __future__ import annotations

from typing import Iterable

from .grafo import Arco


def corte_minimo(
    vertices: Iterable[str],
    arcos_activos: Iterable[Arco],
    s: str,
    t: str,
) -> set[Arco]:
    raise NotImplementedError(
        "Pendiente de implementar por Integrante 2 a partir de la red residual."
    )
