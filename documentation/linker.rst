================================================
Arquitectura de Inyección de Dependencias (Linker)
================================================

:Status: Draft
:Version: 1.0
:Scope: Refactorización de Tests e Integración

Descripción General
==================

Para desacoplar la lógica de procesamiento de los casos de prueba y permitir una mayor flexibilidad en la gestión de dependencias, se ha implementado un patrón de **Inyección de Dependencias** centralizado a través de un objeto llamado ``linker``.

Este enfoque permite que los módulos de test (``test_rst.py``) no dependan directamente de las implementaciones internas (``processor``, ``formatter``, ``cleaner``, etc.), sino que interactúen con una interfaz unificada.

Objetivos del Diseño
====================

1. **Homogeneidad**: Centralizar todas las funciones críticas en un único punto de acceso.
2. **Reducción de Acoplamiento**: Eliminar los múltiples ``imports`` locales dentro de las funciones de test.
3. **Mantenibilidad**: Facilitar futuros cambios en la estructura de archivos sin romper la suite de pruebas.

Implementación Técnica
======================

El objeto ``linker`` actúa como un mediador. En lugar de realizar importaciones directas como:

.. code-block:: python

   from processor import is_structural_break
   self.assertTrue(is_structural_break(line))

Se utiliza el espacio de nombres de ``linker``:

.. code-block:: python

   self.assertTrue(linker.is_structural_break(line))

Funciones Migradas
==================

A continuación se listan las funciones que han sido centralizadas bajo este protocolo:

* **Procesamiento**:
    - ``process_rst_blocks``
    - ``is_structural_break``
    - ``identify_literal_blocks``
    - ``extract_literal_blocks``
    - ``reinject_literal_blocks``
* **Formato y Limpieza**:
    - ``rst_title_formatter``
    - ``clean_line_content``
    - ``filter_and_format_blocks``
* **Referencias**:
    - ``get_document_titles``
    - ``group_refs_blocks``

Impacto en el Desarrollo
========================

- **Legibilidad**: Los archivos de test son más limpios al eliminar bloques de importación repetitivos.
- **Consistencia**: Asegura que tanto el código de producción como el de test utilicen la misma instancia de las funciones, evitando comportamientos inconsistentes.
- **Estandarización**: Cumple con el requisito de descripciones en inglés para mantener la homogeneidad dentro del sistema de administración.