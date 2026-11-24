from __future__ import annotations

import unittest

from src.camino_minimo import camino_minimo
from src.grafo import crear_grafo_inicial, crear_grafo_manual


class TestIntegracionEscenarios(unittest.TestCase):
    def test_tabla_referencia_camino_minimo(self) -> None:
        g0 = crear_grafo_inicial()
        _, d0 = camino_minimo(g0.vertices, g0.arcos_activos, "s", "t")
        self.assertEqual(d0, 3)

        g1 = crear_grafo_inicial()
        g1.bloquear_arco("H", "t")
        _, d1 = camino_minimo(g1.vertices, g1.arcos_activos, "s", "t")
        self.assertEqual(d1, 3)

        g2 = crear_grafo_inicial()
        g2.agregar_arco("A", "t")
        _, d2 = camino_minimo(g2.vertices, g2.arcos_activos, "s", "t")
        self.assertEqual(d2, 2)

        gm = crear_grafo_manual()
        _, dm = camino_minimo(gm.vertices, gm.arcos_activos, "s", "t")
        self.assertEqual(dm, 2)

        g_sin = crear_grafo_inicial()
        for u in ("F", "G", "H"):
            g_sin.bloquear_arco(u, "t")
        camino_sin, d_sin = camino_minimo(g_sin.vertices, g_sin.arcos_activos, "s", "t")
        self.assertIsNone(camino_sin)
        self.assertIsNone(d_sin)


if __name__ == "__main__":
    unittest.main()
