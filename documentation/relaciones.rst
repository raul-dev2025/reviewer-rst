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

Descripción de Modificaciones
=============================

1. **Centralización de Dependencias**: 
   Se han movido todas las importaciones de lógica (``processor``, ``cleaner``, ``formatter``, etc.) al ámbito global del script. Esto elimina la necesidad de realizar importaciones dentro de funciones, resolviendo los conflictos de visibilidad reportados en los tests.

2. **Estandarización de Imports**:
   Se utiliza ahora una carga explícita de módulos completos en lugar de importaciones parciales de funciones, facilitando el mantenimiento de la integridad de las clases y atributos.

3. **Nueva Función de Inicialización**:
   Se ha implementado ``init_environment()`` como el primer paso del flujo de ejecución para preparar rutas y parámetros de configuración de forma aislada.

Impacto en la Arquitectura
==========================

* **Visibilidad**: Los módulos ``reference_processor`` y ``regex`` están ahora disponibles en todo el ciclo de vida del script principal.
* **Mantenibilidad**: Se facilita la depuración de errores estructurales al no depender de cargas condicionales o perezosas (lazy imports).

-----