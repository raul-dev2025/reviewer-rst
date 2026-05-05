===========================================
Relaciones de Módulos - Proyecto review
===========================================

:Autor: Raúl Vílchez
:Fecha: Mayo 2026

Este documento describe la estructura de dependencias y relaciones entre los módulos del proyecto para facilitar la refactorización sin afectar clases ni atributos.

Resumen de Relaciones
=====================

El proyecto se divide principalmente en los siguientes componentes:

Aplicación
----------
- **__init__**: Actualmente se encuentra vacío.
- **review.py**: Script principal.
- **processor.py**: Procesador lógico.
- **formatter.py**: Formateador de salida.
- **reference_processor**: Procesador de referencias.
- **file_manager.py**: Gestor de ficheros.
- **cleaner.py**: Limpieza de datos.
- **regex.py**: Utilidades de expresiones regulares.

Suite de Tests
--------------
- **test_rst.py**: Validaciones de formato rST.
- **test_except.py**: Validaciones de control de excepciones.
- **exceptions.py**: Definición de excepciones personalizadas.
- **run_all_tests.py**: Ejecutor global de la suite.

Tests de Integración
--------------------
- **tests_integration.py**: Módulo de validación de integración que verifica el flujo completo.

Grafo de Dependencias
=====================

A continuación se detalla el flujo de dependencias entre los módulos:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Módulo
     - Depende de
   * - ``review.py``
     - ``file_manager.py``, ``reference_processor``
   * - ``tests_integration.py``
     - ``review.py``, ``file_manager.py``

Plan de Acción para la Centralización
=====================================

1. **Centralización de Imports**: Mover todas las importaciones internas al ámbito global (cabecera).
2. **Modularidad**: Preparar la inicialización en ``review.py``.