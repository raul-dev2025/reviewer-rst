# -*- coding: utf-8 -*-

import unittest

if __name__ == "__main__":
  loader = unittest.TestLoader()
  # Carga archivos de test
  suite = loader.discover(start_dir='.', pattern='test_*.py')

  runner = unittest.TextTestRunner(verbosity=1)
  runner.run(suite)