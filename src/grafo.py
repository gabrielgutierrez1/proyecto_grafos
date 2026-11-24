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
    if vertice == "s":
        return (0, vertice)
    if vertice == "t":
        return (2, vertice)
    return (1, vertice)


def ordenar_vertices(vertices: Iterable[str]) -> list[str]:
    return sorted(vertices, key=_clave_orden)


def construir_adyacencia(
    vertices: Iterable[str],
    arcos_activos: Iterable[Arco],
) -> dict[str, list[str]]:
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
    def __init__(
        self,
        vertices: Iterable[str],
        arcos: Iterable[Arco],
        entrada: str = "s",
        salida: str = "t",
        *,
        es_grafo_inicial: bool = False,
    ) -> None:
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
        return self.arcos - self.bloqueados

    def cambiar_extremos(self, entrada: str, salida: str) -> None:
        if entrada not in self.vertices or salida not in self.vertices:
            raise ValueError("La entrada y la salida deben pertenecer a V.")
        if entrada == salida:
            raise ValueError("La entrada y la salida deben ser distintas (s != t).")
        self.entrada = entrada
        self.salida = salida

    def agregar_arco(self, u: str, v: str) -> None:
        validar_nuevo_arco(self.vertices, self.arcos, u, v)
        self.arcos.add((u, v))

    def bloquear_arco(self, u: str, v: str) -> None:
        if (u, v) not in self.arcos:
            raise ValueError(f"El arco ({u!r}, {v!r}) no existe en el grafo.")
        self.bloqueados.add((u, v))

    def restablecer_arco(self, u: str, v: str) -> None:
        if (u, v) not in self.arcos:
            raise ValueError(f"El arco ({u!r}, {v!r}) no existe en el grafo.")
        self.bloqueados.discard((u, v))

    def restablecer_todos(self) -> None:
        self.bloqueados.clear()

    def lista_adyacencia(self, solo_activos: bool = True) -> dict[str, list[str]]:
        arcos_usar = self.arcos_activos if solo_activos else self.arcos
        return construir_adyacencia(self.vertices, arcos_usar)


def crear_grafo_inicial() -> GrafoLaberinto:
    return GrafoLaberinto(
        VERTICES_INICIALES,
        ARCOS_INICIALES,
        entrada="s",
        salida="t",
        es_grafo_inicial=True,
    )


def crear_grafo_manual() -> GrafoLaberinto:
    return GrafoLaberinto(
        VERTICES_CASO_MANUAL,
        ARCOS_CASO_MANUAL,
        entrada="s",
        salida="t",
        es_grafo_inicial=False,
    )
