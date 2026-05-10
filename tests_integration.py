# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
import os
import file_manager

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.test_dir = "/tmp/findOut"
        # 1. Limpiamos el directorio antes de cada prueba
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        elif os.path.exists(os.path.join(self.test_dir, "referencias.rst")):
            os.remove(os.path.join(self.test_dir, "referencias.rst"))

    @patch('sys.argv', ['review.py', '--seek-refs', 'dummy_file.rst'])
    @patch('file_manager.read_file')
    def test_full_flow_seek_refs(self, mock_load):
        from review import main

        sample_lines = [
            "Referencias",
            "-----------",
            "",
            "[#f1] Almesberger, Werner; \"Booting Linux: The History and the Future\"",
            "    http://www.almesberger.net/cv/papers/ols2k-9.ps.gz",
            "[#f2] newlib package (experimental), with initrd example",
            "    https://www.sourceware.org/newlib/",
            "[#f3] util-linux: Miscellaneous utilities for Linux",
            "    https://www.kernel.org/pub/linux/utils/util-linux/",
            "    [f5] situando en memoria, o trampa de arranque -bootstrapping."
        ]
        mock_load.return_value = "\n".join(sample_lines)

        print("\n--- INICIO DE LA EJECUCIÓN DEL TEST ---")
        main()

        expected_path = os.path.join(self.test_dir, "referencias.rst")

        dir_exists = os.path.exists(self.test_dir)
        print(f"Directorio {self.test_dir} existe: {dir_exists}")

        file_exists = os.path.exists(expected_path)
        print(f"Archivo 'referencias.rst' existe: {file_exists}")

        # Forzamos la comprobación
        self.assertTrue(file_exists, "El archivo 'referencias.rst' no se ha creado en la ruta esperada.")

        with open(expected_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Referencias", content)
            self.assertIn("[#f1]", content)
            self.assertIn("f5", content)

        print(f"\n✅ Integración exitosa y archivo verificado en: {expected_path}")

if __name__ == '__main__':
    unittest.main()