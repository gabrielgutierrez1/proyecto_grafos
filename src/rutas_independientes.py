"""Módulo de rutas independientes (disjuntas en arcos) mediante flujo máximo.

Implementa el algoritmo de Edmonds-Karp con capacidad unitaria (1) por arco
dirigido y la reconstrucción explícita de los caminos dirigidos desde `s`
hasta `t` sin compartir arcos (permitiendo compartir vértices).
"""

from collections import deque


def _clave_orden(vertice):
    """Clave determinista para ordenar vértices de cualquier tipo comparable o mixto."""
    return (str(type(vertice)), str(vertice))


def edmonds_karp_unitario(vertices, arcos_activos, s, t):
    """Calcula el flujo máximo de capacidad unitaria entre `s` y `t`.

    Args:
        vertices: Colección o conjunto de vértices del grafo.
        arcos_activos: Colección o conjunto de tuplas `(u, v)` dirigidas activas.
        s: Vértice origen.
        t: Vértice destino.

    Returns:
        tuple: `(flujo_max, flujo_arcos, residual)` donde:
            - `flujo_max` (int): Cantidad máxima de flujo (número de rutas disjuntas en arcos).
            - `flujo_arcos` (dict[tuple, int]): Mapa `(u, v) -> 1` para arcos activos usados.
            - `residual` (dict[any, dict[any, int]]): Red residual final con capacidades restantes.
    """
    conjunto_vertices = set(vertices)
    if s not in conjunto_vertices or t not in conjunto_vertices or s == t:
        return 0, {}, {}

    # Construir red residual determinista con capacidad 1 para cada arco activo.
    residual = {v: {} for v in conjunto_vertices}
    arcos_validos = set()

    for u, v in sorted(arcos_activos, key=lambda e: (_clave_orden(e[0]), _clave_orden(e[1]))):
        if u in conjunto_vertices and v in conjunto_vertices and u != v:
            arcos_validos.add((u, v))
            residual[u][v] = 1
            if u not in residual[v]:
                residual[v][u] = 0

    # Orden determinista de vecinos por vértice.
    adyacencia = {
        v: sorted(residual[v].keys(), key=_clave_orden)
        for v in conjunto_vertices
    }

    flujo_max = 0

    # Búsqueda de caminos aumentantes mediante BFS (Edmonds-Karp).
    while True:
        padre = {s: None}
        cola = deque([s])

        while cola and t not in padre:
            actual = cola.popleft()
            for vecino in adyacencia[actual]:
                if vecino not in padre and residual[actual].get(vecino, 0) > 0:
                    padre[vecino] = actual
                    if vecino == t:
                        break
                    cola.append(vecino)

        if t not in padre:
            break

        # Con capacidad unitaria, cada camino aumentante aporta exactamente 1 unidad.
        flujo_max += 1
        v = t
        while v != s:
            u = padre[v]
            residual[u][v] -= 1
            residual[v][u] += 1
            v = u

    # Un arco activo (u, v) lleva flujo 1 si su capacidad residual bajó a 0.
    flujo_arcos = {
        (u, v): 1
        for (u, v) in arcos_validos
        if residual[u].get(v, 0) == 0
    }

    return flujo_max, flujo_arcos, residual


def reconstruir_caminos(flujo_arcos, s, t, flujo_max):
    """Reconstruye `flujo_max` caminos dirigidos de `s` a `t` sin arcos repetidos.

    Los caminos pueden compartir vértices, pero nunca comparten arcos.

    Args:
        flujo_arcos: Diccionario con los arcos `(u, v)` que llevan flujo 1.
        s: Vértice origen.
        t: Vértice destino.
        flujo_max: Número esperado de caminos independientes.

    Returns:
        list[list]: Lista de caminos, donde cada camino es una lista de vértices `[s, ..., t]`.
    """
    if flujo_max <= 0:
        return []

    # Grafo dirigido únicamente con los arcos saturados (disponibles para extraer rutas).
    grafo_flujo = {}
    for u, v in sorted(flujo_arcos.keys(), key=lambda e: (_clave_orden(e[0]), _clave_orden(e[1]))):
        grafo_flujo.setdefault(u, []).append(v)

    caminos = []
    for _ in range(flujo_max):
        # BFS determinista sobre los arcos de flujo aún no consumidos.
        padre = {s: None}
        cola = deque([s])
        encontrado = False

        while cola and not encontrado:
            actual = cola.popleft()
            for vecino in grafo_flujo.get(actual, []):
                if vecino not in padre:
                    padre[vecino] = actual
                    if vecino == t:
                        encontrado = True
                        break
                    cola.append(vecino)

        if not encontrado:
            break

        camino = []
        actual = t
        while actual is not None:
            camino.append(actual)
            actual = padre[actual]
        camino.reverse()

        # Consumir los arcos del camino encontrado para que no se reutilicen.
        for i in range(len(camino) - 1):
            u, v = camino[i], camino[i + 1]
            grafo_flujo[u].remove(v)

        caminos.append(camino)

    return caminos
