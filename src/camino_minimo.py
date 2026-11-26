"""Búsqueda por amplitud (BFS) para obtener un camino mínimo en cantidad de arcos.

Implementa desde cero el recorrido por niveles sobre listas de adyacencia y la
reconstrucción de la ruta dirigida mediante predecesores en tiempo O(|V| + |E|).
"""

from __future__ import annotations

from collections import deque
from typing import Iterable

from .grafo import Arco, construir_adyacencia


def _reconstruir_camino(predecesor: dict[str, str | None], destino: str) -> list[str]:
    """Reconstruye la secuencia de vértices desde el origen hasta `destino`.

    Args:
        predecesor: Diccionario que asocia cada vértice visitado con su vértice
            anterior en el árbol BFS (`None` para el origen).
        destino: Vértice final alcanzado por la búsqueda.

    Returns:
        list[str]: Camino dirigido ordenado `[s, ..., destino]`.
    """
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
    """Calcula un camino dirigido de `s` a `t` con el menor número de arcos usando BFS.

    Args:
        vertices: Colección iterable de vértices del grafo.
        arcos_activos: Colección iterable de arcos dirigidos `(u, v)` habilitados.
        s: Vértice de entrada.
        t: Vértice de salida (distinto de `s`).

    Returns:
        tuple[list[str] | None, int | None]: Par `(camino, longitud)` donde `camino`
            es la lista de vértices `[s, ..., t]` y `longitud` es `len(camino) - 1`.
            Si `t` no es alcanzable desde `s`, retorna `(None, None)` sin asignar
            longitud numérica. Lanza `ValueError` si `s == t` o algún extremo no
            pertenece a `vertices`.
    """
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
    """Convierte el resultado de `camino_minimo` en una representación legible.

    Args:
        camino: Lista ordenada de vértices del camino mínimo, o `None` si no existe.
        longitud: Cantidad de arcos del camino, o `None` si no existe conexión.

    Returns:
        str: Cadena `'Sin camino'` cuando no hay conexión, o la secuencia de
            vértices junto con su longitud en arcos.
    """
    if camino is None or longitud is None:
        return "Sin camino"
    ruta_texto = " -> ".join(camino)
    return f"{ruta_texto} (longitud: {longitud} arcos)"
