"""Modelación matemática del laberinto como grafo dirigido G = (V, E).

Define la red principal G0 (10 vértices y 18 arcos), el caso independiente
manual Gm (5 vértices y 7 arcos), el orden determinista de vértices y las
reglas de validación para modificaciones interactivas sobre arcos activos.
"""

from __future__ import annotations

from typing import Iterable

Arco = tuple[str, str]

VERTICES_INICIALES: frozenset[str] = frozenset(
    {"s", "A", "B", "C", "D", "E", "F", "G", "H", "t"}
)

ARCOS_INICIALES: frozenset[Arco] = frozenset(
    {
        ("s", "A"),
        ("s", "B"),
        ("s", "C"),
        ("A", "D"),
        ("A", "E"),
        ("B", "D"),
        ("B", "E"),
        ("B", "F"),
        ("C", "E"),
        ("C", "F"),
        ("D", "G"),
        ("D", "H"),
        ("E", "G"),
        ("E", "H"),
        ("F", "H"),
        ("F", "t"),
        ("G", "t"),
        ("H", "t"),
    }
)

POSICIONES_SUGERIDAS: dict[str, tuple[float, float]] = {
    "s": (0.05, 0.50),
    "A": (0.27, 0.82),
    "B": (0.27, 0.50),
    "C": (0.27, 0.18),
    "D": (0.50, 0.82),
    "E": (0.50, 0.50),
    "F": (0.50, 0.18),
    "G": (0.73, 0.68),
    "H": (0.73, 0.32),
    "t": (0.95, 0.50),
}

VERTICES_CASO_MANUAL: frozenset[str] = frozenset({"s", "A", "B", "C", "t"})

ARCOS_CASO_MANUAL: frozenset[Arco] = frozenset(
    {
        ("s", "A"),
        ("s", "B"),
        ("A", "C"),
        ("A", "t"),
        ("B", "C"),
        ("B", "t"),
        ("C", "t"),
    }
)


def _clave_orden(vertice: str) -> tuple[int, str]:
    """Asigna prioridad canónica a un vértice ('s' primero, intermedios, 't' al final).

    Args:
        vertice: Identificador del vértice a evaluar.

    Returns:
        tuple[int, str]: Par `(grupo, nombre)` para ordenación determinista.
    """
    if vertice == "s":
        return (0, vertice)
    if vertice == "t":
        return (2, vertice)
    return (1, vertice)


def ordenar_vertices(vertices: Iterable[str]) -> list[str]:
    """Ordena una colección de vértices de forma determinista y reproducible.

    Args:
        vertices: Colección iterable de identificadores de vértices.

    Returns:
        list[str]: Lista de vértices con `'s'` al inicio, nodos intermedios
            ordenados alfabéticamente y `'t'` al final.
    """
    return sorted(vertices, key=_clave_orden)


def construir_adyacencia(
    vertices: Iterable[str],
    arcos_activos: Iterable[Arco],
) -> dict[str, list[str]]:
    """Construye la lista de adyacencia saliente usando únicamente arcos activos.

    Args:
        vertices: Colección iterable con los vértices válidos del grafo.
        arcos_activos: Colección iterable de pares ordenados `(u, v)` activos.

    Returns:
        dict[str, list[str]]: Diccionario que asocia cada vértice con su lista
            ordenada de vecinos salientes alcanzables.
    """
    conjunto_v = set(vertices)
    adyacencia: dict[str, set[str]] = {v: set() for v in conjunto_v}

    for u, v in arcos_activos:
        if u in conjunto_v and v in conjunto_v:
            adyacencia[u].add(v)

    return {u: ordenar_vertices(vecinos) for u, vecinos in adyacencia.items()}


def validar_nuevo_arco(
    vertices: set[str],
    arcos_existentes: set[Arco],
    u: str,
    v: str,
) -> None:
    """Verifica que un pasillo candidato `(u, v)` cumpla las restricciones de la red.

    Rechaza extremos fuera de `V`, lazos `(v, v)`, arcos repetidos y arcos recíprocos.

    Args:
        vertices: Conjunto de vértices existentes en el grafo.
        arcos_existentes: Conjunto actual de arcos registrados en el grafo.
        u: Vértice origen del nuevo pasillo.
        v: Vértice destino del nuevo pasillo.

    Returns:
        None: No retorna valor; lanza `ValueError` si alguna regla se incumple.
    """
    if u not in vertices or v not in vertices:
        raise ValueError(f"Ambos extremos deben pertenecer a V: ({u!r}, {v!r}).")
    if u == v:
        raise ValueError(f"No se permiten lazos sobre un mismo vértice: ({u!r}, {v!r}).")
    if (u, v) in arcos_existentes:
        raise ValueError(f"El arco ({u!r}, {v!r}) ya existe en la red.")
    if (v, u) in arcos_existentes:
        raise ValueError(
            f"No se permiten arcos recíprocos: ya existe ({v!r}, {u!r})."
        )


def validar_grafo_inicial(
    vertices: set[str],
    arcos: Iterable[Arco],
    s: str = "s",
    t: str = "t",
) -> None:
    """Comprueba todas las restricciones formales exigidas para la red inicial G0.

    Verifica `10 <= |V| <= 12`, `14 <= |E| <= 20`, `s != t`, ausencia de vértices
    aislados y validez estructural de cada arco.

    Args:
        vertices: Conjunto de vértices del grafo inicial.
        arcos: Colección iterable de arcos dirigidos iniciales.
        s: Vértice de entrada.
        t: Vértice de salida.

    Returns:
        None: No retorna valor; lanza `ValueError` si alguna restricción falla.
    """
    lista_arcos = list(arcos)
    num_v = len(vertices)
    num_e = len(lista_arcos)

    if not (10 <= num_v <= 12):
        raise ValueError(f"El grafo inicial requiere entre 10 y 12 vértices (tiene {num_v}).")
    if not (14 <= num_e <= 20):
        raise ValueError(f"El grafo inicial requiere entre 14 y 20 arcos (tiene {num_e}).")
    if s not in vertices or t not in vertices:
        raise ValueError("La entrada 's' y la salida 't' deben pertenecer a V.")
    if s == t:
        raise ValueError("La entrada y la salida deben ser distintas (s != t).")

    arcos_vistos: set[Arco] = set()
    incidentes: set[str] = set()

    for u, v in lista_arcos:
        validar_nuevo_arco(vertices, arcos_vistos, u, v)
        arcos_vistos.add((u, v))
        incidentes.add(u)
        incidentes.add(v)

    aislados = vertices - incidentes
    if aislados:
        raise ValueError(
            f"No se permiten vértices aislados: {ordenar_vertices(aislados)}."
        )


class GrafoLaberinto:
    """Modelo de estado del laberinto dirigido con soporte de bloqueos y edición."""

    def __init__(
        self,
        vertices: Iterable[str],
        arcos: Iterable[Arco],
        entrada: str = "s",
        salida: str = "t",
        *,
        es_grafo_inicial: bool = False,
    ) -> None:
        """Inicializa el grafo dirigido validando sus vértices, arcos y extremos.

        Args:
            vertices: Colección iterable de vértices del laberinto.
            arcos: Colección iterable de pares ordenados `(u, v)`.
            entrada: Vértice inicial seleccionado (`s` por defecto).
            salida: Vértice destino seleccionado (`t` por defecto).
            es_grafo_inicial: Si es `True`, exige además las cotas iniciales de G0.

        Returns:
            None.
        """
        self.vertices: set[str] = set(vertices)
        lista_arcos = list(arcos)

        if es_grafo_inicial:
            validar_grafo_inicial(self.vertices, lista_arcos, entrada, salida)
            self.arcos: set[Arco] = set(lista_arcos)
        else:
            if entrada not in self.vertices or salida not in self.vertices:
                raise ValueError("La entrada y la salida deben pertenecer a V.")
            if entrada == salida:
                raise ValueError("La entrada y la salida deben ser distintas.")
            self.arcos = set()
            for u, v in lista_arcos:
                validar_nuevo_arco(self.vertices, self.arcos, u, v)
                self.arcos.add((u, v))

        self.bloqueados: set[Arco] = set()
        self.entrada: str = entrada
        self.salida: str = salida

    @property
    def arcos_activos(self) -> set[Arco]:
        """Obtiene el subconjunto de pasillos habilitados (`arcos - bloqueados`).

        Returns:
            set[Arco]: Conjunto de arcos activos disponibles para el recorrido.
        """
        return self.arcos - self.bloqueados

    def cambiar_extremos(self, entrada: str, salida: str) -> None:
        """Actualiza los vértices de entrada y salida verificando que sean distintos.

        Args:
            entrada: Nuevo vértice origen `s`.
            salida: Nuevo vértice destino `t`.

        Returns:
            None: Lanza `ValueError` si algún extremo no existe o si coinciden.
        """
        if entrada not in self.vertices or salida not in self.vertices:
            raise ValueError("La entrada y la salida deben pertenecer a V.")
        if entrada == salida:
            raise ValueError("La entrada y la salida deben ser distintas (s != t).")
        self.entrada = entrada
        self.salida = salida

    def agregar_arco(self, u: str, v: str) -> None:
        """Incorpora un nuevo pasillo dirigido `(u, v)` tras validar las reglas del modelo.

        Args:
            u: Vértice origen del pasillo.
            v: Vértice destino del pasillo.

        Returns:
            None: Lanza `ValueError` si el arco es lazo, duplicado, recíproco o inválido.
        """
        validar_nuevo_arco(self.vertices, self.arcos, u, v)
        self.arcos.add((u, v))

    def bloquear_arco(self, u: str, v: str) -> None:
        """Bloquea temporalmente un pasillo existente excluyéndolo de `arcos_activos`.

        Args:
            u: Vértice origen del arco a bloquear.
            v: Vértice destino del arco a bloquear.

        Returns:
            None: Lanza `ValueError` si el arco no pertenece a `self.arcos`.
        """
        if (u, v) not in self.arcos:
            raise ValueError(f"El arco ({u!r}, {v!r}) no existe en el grafo.")
        self.bloqueados.add((u, v))

    def restablecer_arco(self, u: str, v: str) -> None:
        """Reactiva un pasillo previamente bloqueado devolviéndolo a `arcos_activos`.

        Args:
            u: Vértice origen del arco a restablecer.
            v: Vértice destino del arco a restablecer.

        Returns:
            None: Lanza `ValueError` si el arco no pertenece a `self.arcos`.
        """
        if (u, v) not in self.arcos:
            raise ValueError(f"El arco ({u!r}, {v!r}) no existe en el grafo.")
        self.bloqueados.discard((u, v))

    def restablecer_todos(self) -> None:
        """Elimina todos los bloqueos temporales activos de la red.

        Returns:
            None.
        """
        self.bloqueados.clear()

    def lista_adyacencia(self, solo_activos: bool = True) -> dict[str, list[str]]:
        """Genera la lista de adyacencia saliente ordenada del grafo.

        Args:
            solo_activos: Si es `True`, considera únicamente `arcos_activos`;
                si es `False`, incluye también los arcos bloqueados.

        Returns:
            dict[str, list[str]]: Mapa de cada vértice hacia sus vecinos ordenados.
        """
        arcos_usar = self.arcos_activos if solo_activos else self.arcos
        return construir_adyacencia(self.vertices, arcos_usar)


def crear_grafo_inicial() -> GrafoLaberinto:
    """Construye y valida la configuración principal G0 de 10 vértices y 18 arcos.

    Returns:
        GrafoLaberinto: Instancia inicializada con `VERTICES_INICIALES` y `ARCOS_INICIALES`.
    """
    return GrafoLaberinto(
        VERTICES_INICIALES,
        ARCOS_INICIALES,
        entrada="s",
        salida="t",
        es_grafo_inicial=True,
    )


def crear_grafo_manual() -> GrafoLaberinto:
    """Construye el caso independiente Gm de 5 vértices y 7 arcos resuelto a mano.

    Returns:
        GrafoLaberinto: Instancia inicializada con `VERTICES_CASO_MANUAL` y `ARCOS_CASO_MANUAL`.
    """
    return GrafoLaberinto(
        VERTICES_CASO_MANUAL,
        ARCOS_CASO_MANUAL,
        entrada="s",
        salida="t",
        es_grafo_inicial=False,
    )
