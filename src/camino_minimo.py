from __future__ import annotations

from collections import deque
from typing import Iterable

from .grafo import Arco, construir_adyacencia


def _reconstruir_camino(predecesor: dict[str, str | None], destino: str) -> list[str]:
    camino_inverso: list[str] = []
    actual: str | None = destino

    while actual is not None:
        camino_inverso.append(actual)
        actual = predecesor[actual]

    camino_inverso.reverse()
    return camino_inverso


def camino_minimo(
    vertices: Iterable[str],
    arcos_activos: Iterable[Arco],
    s: str,
    t: str,
) -> tuple[list[str] | None, int | None]:
    conjunto_v = set(vertices)
    if s not in conjunto_v or t not in conjunto_v:
        raise ValueError(f"Los extremos deben pertenecer a V: s={s!r}, t={t!r}.")
    if s == t:
        raise ValueError("La entrada y la salida deben ser distintas (s != t).")

    adyacencia = construir_adyacencia(conjunto_v, arcos_activos)

    cola: deque[str] = deque([s])
    predecesor: dict[str, str | None] = {s: None}

    while cola:
        u = cola.popleft()

        for v in adyacencia[u]:
            if v not in predecesor:
                predecesor[v] = u
                if v == t:
                    camino = _reconstruir_camino(predecesor, t)
                    return camino, len(camino) - 1
                cola.append(v)

    return None, None


def formatear_resultado_camino(
    camino: list[str] | None,
    longitud: int | None,
) -> str:
    if camino is None or longitud is None:
        return "Sin camino"
    ruta_texto = " -> ".join(camino)
    return f"{ruta_texto} (longitud: {longitud} arcos)"
