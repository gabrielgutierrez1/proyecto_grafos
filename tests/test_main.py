"""Comprueba los puntos de entrada sin necesitar una pantalla."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class TestInicio(unittest.TestCase):
    def test_archivo_directo_y_modulo(self):
        raiz = Path(__file__).resolve().parents[1]
        modulo = subprocess.run(
            [sys.executable, "-m", "src.main", "--consola"],
            cwd=raiz, capture_output=True, text=True, check=True,
        )
        with tempfile.TemporaryDirectory() as directorio:
            archivo = subprocess.run(
                [sys.executable, str(raiz / "src" / "main.py"), "--consola"],
                cwd=directorio, capture_output=True, text=True, check=True,
            )
        self.assertEqual(archivo.stdout, modulo.stdout)
        self.assertIn("G0", archivo.stdout)
        self.assertIn("G2", archivo.stdout)
        self.assertEqual(archivo.stderr, "")
