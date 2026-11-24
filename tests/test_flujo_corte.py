from __future__ import annotations

import unittest

from src.grafo import crear_grafo_inicial, crear_grafo_manual
from src.rutas_independientes import rutas_y_corte


@unittest.skip("Pendiente de implementar rutas_y_corte por Integrante 2")
class TestFlujoCorte(unittest.TestCase):
    def test_red_original_g0(self) -> None:
        g0 = crear_grafo_inicial()
        caminos, corte = rutas_y_corte(g0.vertices, g0.arcos_activos, "s", "t")
        self.assertEqual(len(caminos), 3)
        self.assertEqual(len(corte), 3)

    def test_caso_manual_cinco_vertices(self) -> None:
        gm = crear_grafo_manual()
        caminos, corte = rutas_y_corte(gm.vertices, gm.arcos_activos, "s", "t")
        self.assertEqual(len(caminos), 2)
        self.assertEqual(len(corte), 2)

    def test_red_sin_conexion(self) -> None:
        g = crear_grafo_inicial()
        for v in ("A", "B", "C"):
            g.bloquear_arco("s", v)
        caminos, corte = rutas_y_corte(g.vertices, g.arcos_activos, "s", "t")
        self.assertEqual(caminos, [])
        self.assertEqual(corte, set())


if __name__ == "__main__":
    unittest.main()
