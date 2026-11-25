"""Módulo de corte mínimo de arcos e integración de rutas y corte.

Identifica un conjunto mínimo de arcos activos cuyo bloqueo desconecta `t`
desde `s`, utilizando la red residual final de Edmonds-Karp.
"""

from collections import deque

from src.rutas_independientes import (
    _clave_orden,
    edmonds_karp_unitario,
    reconstruir_caminos,
)


def obtener_corte_minimo(vertices, arcos_activos, residual, s):
    """Obtiene el corte mínimo `(S, T)` de arcos activos a partir de la red residual.

    Realiza un BFS desde `s` siguiendo únicamente arcos con capacidad residual > 0.
    Todo arco activo `(u, v)` con `u` alcanzable y `v` no alcanzable pertenece al corte.

    Args:
        vertices: Colección o conjunto de vértices del grafo.
        arcos_activos: Colección o conjunto de tuplas `(u, v)` dirigidas activas.
        residual: Red residual final devuelta por `edmonds_karp_unitario`.
        s: Vértice origen.

    Returns:
        set[tuple]: Conjunto de arcos `(u, v)` que forman el corte mínimo.
    """
    conjunto_vertices = set(vertices)
    if s not in conjunto_vertices or not residual:
        return set()

    alcanzables = {s}
    cola = deque([s])

    while cola:
        actual = cola.popleft()
        vecinos = sorted(residual.get(actual, {}).keys(), key=_clave_orden)
        for vecino in vecinos:
            if vecino not in alcanzables and residual[actual].get(vecino, 0) > 0:
                alcanzables.add(vecino)
                cola.append(vecino)

    corte = {
        (u, v)
        for (u, v) in arcos_activos
        if u in conjunto_vertices
        and v in conjunto_vertices
        and u in alcanzables
        and v not in alcanzables
    }
    return corte


def rutas_y_corte(vertices, arcos_activos, s, t):
    """Calcula el máximo número de rutas sin arcos compartidos y su corte mínimo.

    Contrato principal del proyecto:
    - Si `s == t`, `s` o `t` no pertenecen a `vertices`, o `t` no es alcanzable
      desde `s`, retorna `([], set())`.
    - En caso contrario, retorna `(caminos, corte)` donde `len(caminos) == len(corte)`.

    Args:
        vertices: Colección o conjunto de vértices.
        arcos_activos: Colección o conjunto de tuplas `(u, v)` dirigidas activas.
        s: Vértice origen.
        t: Vértice destino.

    Returns:
        tuple[list[list], set[tuple]]: `(caminos, corte)`.
    """
    conjunto_vertices = set(vertices)
    if s not in conjunto_vertices or t not in conjunto_vertices or s == t:
        return [], set()

    flujo_max, flujo_arcos, residual = edmonds_karp_unitario(
        conjunto_vertices, arcos_activos, s, t
    )

    if flujo_max == 0:
        return [], set()

    caminos = reconstruir_caminos(flujo_arcos, s, t, flujo_max)
    corte = obtener_corte_minimo(conjunto_vertices, arcos_activos, residual, s)

    return caminos, corte
