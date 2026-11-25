"""Pruebas unitarias para rutas independientes (disjuntas en arcos) y corte mínimo."""

import unittest

from src.corte_minimo import rutas_y_corte


class TestFlujoCorte(unittest.TestCase):
    """Valida el contrato de `rutas_y_corte` y el teorema flujo-máximo corte-mínimo."""

    def _validar_resultado(self, vertices, arcos_activos, s, t, caminos, corte):
        """Verifica invariantes: caminos dirigidos válidos, sin arcos repetidos y |caminos| == |corte|."""
        conjunto_vertices = set(vertices)
        conjunto_arcos = set(arcos_activos)
        arcos_usados = set()

        for camino in caminos:
            self.assertGreaterEqual(len(camino), 2)
            self.assertEqual(camino[0], s)
            self.assertEqual(camino[-1], t)
            for i in range(len(camino) - 1):
                u, v = camino[i], camino[i + 1]
                self.assertIn(u, conjunto_vertices)
                self.assertIn(v, conjunto_vertices)
                self.assertIn((u, v), conjunto_arcos)
                self.assertNotIn((u, v), arcos_usados, f"Arco repetido: {(u, v)}")
                arcos_usados.add((u, v))

        self.assertTrue(corte.issubset(conjunto_arcos))
        self.assertEqual(len(caminos), len(corte))

    def test_rutas_comparten_vertice_pero_no_arcos(self):
        """Dos caminos pueden cruzarse en un vértice intermedio si usan arcos distintos."""
        vertices = {"S", "A", "B", "C", "D", "T"}
        arcos = {
            ("S", "A"), ("S", "B"),
            ("A", "C"), ("B", "C"),
            ("C", "D"), ("C", "T"),
            ("D", "T"),
        }
        caminos, corte = rutas_y_corte(vertices, arcos, "S", "T")

        self._validar_resultado(vertices, arcos, "S", "T", caminos, corte)
        self.assertEqual(len(caminos), 2)

        # Verificar que ambos caminos pasan por el vértice compartido "C".
        self.assertTrue(all("C" in camino for camino in caminos))

    def test_pasillos_bloqueados_recalcula_rutas_y_corte(self):
        """Al bloquear un arco activo, disminuyen las rutas y cambia el corte mínimo."""
        vertices = {"S", "A", "B", "T"}
        arcos = {
            ("S", "A"), ("A", "T"),
            ("S", "B"), ("B", "T"),
        }

        caminos_inicial, corte_inicial = rutas_y_corte(vertices, arcos, "S", "T")
        self._validar_resultado(vertices, arcos, "S", "T", caminos_inicial, corte_inicial)
        self.assertEqual(len(caminos_inicial), 2)

        # Bloqueamos el pasillo ("S", "B")
        bloqueados = {("S", "B")}
        arcos_activos = arcos - bloqueados

        caminos_post, corte_post = rutas_y_corte(vertices, arcos_activos, "S", "T")
        self._validar_resultado(vertices, arcos_activos, "S", "T", caminos_post, corte_post)
        self.assertEqual(len(caminos_post), 1)
        self.assertEqual(caminos_post[0], ["S", "A", "T"])

    def test_red_sin_conexion(self):
        """Si t no es alcanzable desde s, o s == t, o faltan vértices, retorna ([], set())."""
        vertices = {"S", "A", "B", "T"}
        arcos = {("S", "A"), ("B", "T")}

        self.assertEqual(rutas_y_corte(vertices, arcos, "S", "T"), ([], set()))
        self.assertEqual(rutas_y_corte(vertices, arcos, "S", "S"), ([], set()))
        self.assertEqual(rutas_y_corte(vertices, arcos, "X", "T"), ([], set()))
        self.assertEqual(rutas_y_corte(vertices, arcos, "S", "Y"), ([], set()))


if __name__ == "__main__":
    unittest.main()
