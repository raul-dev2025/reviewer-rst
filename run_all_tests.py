# -*- coding: utf-8 -*-
# Copyright (c) 2026 Raúl Vílchez Ruiz <r4u1974@gmail.com>
# Distributed under the terms of the MIT License.
# See LICENSE file in the project root for full license information.


import unittest

if __name__ == "__main__":
  loader = unittest.TestLoader()
  # Carga archivos de test
  suite = loader.discover(start_dir='.', pattern='test_*.py')

  runner = unittest.TextTestRunner(verbosity=1)
  runner.run(suite)