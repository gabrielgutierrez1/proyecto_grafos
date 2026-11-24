from __future__ import annotations

import unittest

from src.camino_minimo import camino_minimo, formatear_resultado_camino
from src.grafo import (
    ARCOS_INICIALES,
    VERTICES_INICIALES,
    crear_grafo_inicial,
    crear_grafo_manual,
    validar_grafo_inicial,
)


class TestModelacionGrafo(unittest.TestCase):

    def test_grafo_inicial_cumple_restricciones_formales(self) -> None:
        grafo = crear_grafo_inicial()
        self.assertEqual(len(grafo.vertices), 10)
        self.assertEqual(len(grafo.arcos), 18)
        self.assertEqual(grafo.arcos_activos, set(ARCOS_INICIALES))
        self.assertNotEqual(grafo.entrada, grafo.salida)

        rutas = [
            ["s", "B", "F", "t"],
            ["s", "A", "D", "G", "t"],
            ["s", "C", "E", "H", "t"],
        ]
        arcos_usados: set[tuple[str, str]] = set()
        for ruta in rutas:
            for u, v in zip(ruta, ruta[1:]):
                self.assertIn((u, v), grafo.arcos_activos)
                self.assertNotIn((u, v), arcos_usados)
                arcos_usados.add((u, v))

    def test_rechaza_lazos_duplicados_reciprocos_y_vertices_invalidos(self) -> None:
        grafo = crear_grafo_inicial()

        with self.assertRaises(ValueError):
            grafo.agregar_arco("A", "A")
        with self.assertRaises(ValueError):
            grafo.agregar_arco("s", "A")
        with self.assertRaises(ValueError):
            grafo.agregar_arco("A", "s")
        with self.assertRaises(ValueError):
            grafo.agregar_arco("A", "Z")

    def test_rechaza_vertice_aislado_y_cardinalidad_fuera_de_rango(self) -> None:
        with self.assertRaises(ValueError):
            validar_grafo_inicial({"s", "A", "t"}, [("s", "A"), ("A", "t")])

        vertices_con_aislado = set(VERTICES_INICIALES) | {"X"}
        with self.assertRaises(ValueError):
            validar_grafo_inicial(vertices_con_aislado, ARCOS_INICIALES)

    def test_bloqueo_restablecimiento_y_cambio_extremos(self) -> None:
        grafo = crear_grafo_inicial()
        grafo.bloquear_arco("H", "t")
        self.assertNotIn(("H", "t"), grafo.arcos_activos)
        self.assertEqual(len(grafo.arcos_activos), 17)

        grafo.restablecer_arco("H", "t")
        self.assertIn(("H", "t"), grafo.arcos_activos)
        self.assertEqual(len(grafo.arcos_activos), 18)

        grafo.cambiar_extremos("A", "H")
        self.assertEqual((grafo.entrada, grafo.salida), ("A", "H"))

        with self.assertRaises(ValueError):
            grafo.cambiar_extremos("A", "A")


class TestCaminoMinimoBFS(unittest.TestCase):

    def test_escenarios_del_informe_y_caso_manual(self) -> None:
        g0 = crear_grafo_inicial()
        camino_0, dist_0 = camino_minimo(g0.vertices, g0.arcos_activos, "s", "t")
        self.assertEqual(camino_0, ["s", "B", "F", "t"])
        self.assertEqual(dist_0, 3)

        g1 = crear_grafo_inicial()
        g1.bloquear_arco("H", "t")
        camino_1, dist_1 = camino_minimo(g1.vertices, g1.arcos_activos, "s", "t")
        self.assertEqual(camino_1, ["s", "B", "F", "t"])
        self.assertEqual(dist_1, 3)

        g2 = crear_grafo_inicial()
        g2.agregar_arco("A", "t")
        camino_2, dist_2 = camino_minimo(g2.vertices, g2.arcos_activos, "s", "t")
        self.assertEqual(camino_2, ["s", "A", "t"])
        self.assertEqual(dist_2, 2)

        gm = crear_grafo_manual()
        camino_m, dist_m = camino_minimo(gm.vertices, gm.arcos_activos, "s", "t")
        self.assertEqual(camino_m, ["s", "A", "t"])
        self.assertEqual(dist_m, 2)

    def test_multiples_caminos_minimos_y_reproducibilidad(self) -> None:
        vertices = {"s", "A", "B", "C", "t"}
        arcos = {("s", "B"), ("s", "A"), ("A", "t"), ("B", "t"), ("s", "C"), ("C", "B")}

        camino, longitud = camino_minimo(vertices, arcos, "s", "t")
        self.assertEqual(longitud, 2)
        self.assertEqual(camino, ["s", "A", "t"])

    def test_destino_inalcanzable_retorna_none_sin_longitud_numerica(self) -> None:
        grafo = crear_grafo_inicial()
        for vecino in ("A", "B", "C"):
            grafo.bloquear_arco("s", vecino)

        camino, longitud = camino_minimo(grafo.vertices, grafo.arcos_activos, "s", "t")
        self.assertIsNone(camino)
        self.assertIsNone(longitud)
        self.assertEqual(formatear_resultado_camino(camino, longitud), "Sin camino")

    def test_respeta_direccion_de_arcos_y_valida_extremos(self) -> None:
        grafo = crear_grafo_inicial()
        camino_inv, longitud_inv = camino_minimo(
            grafo.vertices, grafo.arcos_activos, "t", "s"
        )
        self.assertEqual((camino_inv, longitud_inv), (None, None))

        with self.assertRaises(ValueError):
            camino_minimo(grafo.vertices, grafo.arcos_activos, "s", "s")
        with self.assertRaises(ValueError):
            camino_minimo(grafo.vertices, grafo.arcos_activos, "s", "NODO_INEXISTENTE")


if __name__ == "__main__":
    unittest.main()
