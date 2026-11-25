"""Verifica integración y, cuando hay pantalla, controles reales de Tkinter."""
import unittest
from unittest.mock import patch

from src.camino_minimo import camino_minimo
from src.escenarios import calcular_resultado, crear_escenarios
from src.grafo import crear_grafo_inicial


class TestEscenariosInterfaz(unittest.TestCase):
    def test_resultados_y_certificados(self):
        for (nombre, grafo), longitud, cantidad in zip(crear_escenarios(), (3, 3, 2), (3, 2, 3)):
            with self.subTest(escenario=nombre):
                r = calcular_resultado(grafo)
                self.assertEqual(r.longitud, longitud)
                self.assertEqual(len(r.rutas), cantidad)
                self.assertEqual(len(r.corte), cantidad)
                usados = set()
                for ruta in r.rutas:
                    self.assertEqual((ruta[0], ruta[-1]), (grafo.entrada, grafo.salida))
                    arcos = set(zip(ruta, ruta[1:]))
                    self.assertTrue(arcos <= grafo.arcos_activos)
                    self.assertFalse(arcos & usados)
                    usados.update(arcos)
                self.assertEqual(camino_minimo(grafo.vertices, grafo.arcos_activos-r.corte, grafo.entrada, grafo.salida), (None, None))

    def test_extremos_fijos_y_escenarios_independientes(self):
        escenarios = crear_escenarios("A", "H")
        for _, grafo in escenarios:
            self.assertEqual((grafo.entrada, grafo.salida), ("A", "H"))
        self.assertEqual(escenarios[0][1].bloqueados, set())
        self.assertNotIn(("A", "t"), escenarios[0][1].arcos)
        self.assertEqual(escenarios[2][1].bloqueados, set())
        with self.assertRaises(ValueError):
            crear_escenarios("s", "s")

    def test_desconexion_y_restablecimiento(self):
        grafo = crear_grafo_inicial()
        for u in ("F", "G", "H"):
            grafo.bloquear_arco(u, "t")
        r = calcular_resultado(grafo)
        self.assertEqual((r.camino, r.longitud, r.rutas, r.corte), (None, None, [], set()))
        grafo.restablecer_arco("F", "t")
        self.assertEqual(len(calcular_resultado(grafo).rutas), 1)


class TestControlesTk(unittest.TestCase):
    def setUp(self):
        try:
            import tkinter as tk
        except ImportError:
            self.skipTest("Tkinter no está instalado")
        try:
            self.raiz = tk.Tk()
        except tk.TclError:
            self.skipTest("No hay pantalla disponible para probar los controles")
        self.addCleanup(self.raiz.destroy)
        self.raiz.withdraw()
        from src.interfaz import InterfazLaberinto
        self.ui = InterfazLaberinto(self.raiz)

    def test_edicion_recalculo_y_validaciones(self):
        self.assertEqual(str(self.ui.botones_pasillo["restablecer_arco"]["state"]), "disabled")
        self.ui.modificar("bloquear_arco")
        self.assertEqual(str(self.ui.botones_pasillo["bloquear_arco"]["state"]), "disabled")
        self.assertEqual(str(self.ui.botones_pasillo["restablecer_arco"]["state"]), "normal")
        self.assertEqual([valor.get() for valor in self.ui.metricas], ["—"] * 3)
        self.assertIsNone(self.ui.resultado)
        self.ui.calcular()
        self.assertEqual(len(self.ui.resultado.rutas), 2)
        self.assertEqual([valor.get() for valor in self.ui.metricas], ["3", "2", "2"])
        self.ui.modificar("restablecer_arco")
        self.ui.calcular()
        self.assertEqual(len(self.ui.resultado.rutas), 3)
        self.ui.origen.set("A")
        self.ui.modificar("agregar_arco")
        self.ui.calcular()
        self.assertEqual(self.ui.resultado.longitud, 2)
        with patch("src.interfaz.messagebox.showerror") as aviso:
            self.ui.modificar("agregar_arco")
            aviso.assert_called_once()
        for modo in self.ui.MODOS:
            self.ui.modo.set(modo)
            self.ui.dibujar()
        self.assertTrue(self.ui.canvas.find_all())

    def test_extremos_y_carga(self):
        with patch("src.interfaz.messagebox.showerror") as aviso:
            self.ui.salida.set("s")
            self.ui._cambiar_extremos()
            aviso.assert_called_once()
        self.assertEqual(self.ui.salida.get(), "t")
        self.ui.entrada.set("A")
        self.ui._cambiar_extremos()
        self.assertIsNone(self.ui.resultado)
        self.assertFalse(self.ui.tabla.get_children())
        self.ui.escenario.set("G1 · Bloquear H → t")
        self.ui.cargar_escenario()
        self.assertEqual(self.ui.grafo.entrada, "A")
        self.assertEqual(len(self.ui.tabla.get_children()), 3)
