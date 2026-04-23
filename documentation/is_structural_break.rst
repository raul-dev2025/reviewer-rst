==========================================
Documentación Técnica: is_structural_break
==========================================

:Módulo: processor.py
:Función: is_structural_break
:Arquitectura: Bimodal (Standard / Seek-Refs)
:Estado: Fase 3 - Integración Estructural

Descripción
===========

Esta función actúa como el "vigía" del procesador. Su objetivo principal es determinar si la línea actual representa un punto de ruptura en el flujo de texto plano para activar la captura de un bloque especializado.

Firma de la Función
===================

.. code-cell:: python

   def is_structural_break(line, seek_refs=False):
       """
       Determina si la línea actual marca el inicio de un bloque de interés.
       Retorna un booleano para simplificar el flujo de control.
       """

Lógica de Operación
===================

El comportamiento de la función varía según el flag de ejecución:

Modo Extracción de Referencias (seek_refs=True)
-----------------------------------------------

En este modo, la función se vuelve "monotemática" para evitar ruido estructural.

* **Detección de Títulos:** Identifica secciones maestras mediante patrones de texto clave como ``Referencias``, ``Recursos`` o ``Agradecimientos``.
* **Detección de Notas al Pie:** Localiza anclajes específicos de rST (p.ej., ``[#f1]``) siempre que se encuentren al inicio de la línea o precedidos por la directiva de puntos.
* **Propósito:** Activar el agrupamiento de bloques bibliográficos ignorando el contenido del cuerpo del documento.

Modo Estándar (seek_refs=False)
-------------------------------

Protege la infraestructura del documento rST detectando disparadores de formato:

* **Directivas (.. ):** Identifica el inicio de comentarios, avisos o inserción de imágenes.
* **Campos de Metadata (   :):** Detecta bloques de atributos indentados (como autoría o versión).
* **Bloques Literales (::):** Dispara la mecánica de preservación absoluta para código fuente o ejemplos literales.

Análisis de Retorno
===================

La función encapsula el resultado en un tipo ``bool``. Esto permite:

1. **Simplicidad:** El orquestador solo necesita saber si "debe romper" la secuencia actual.
2. **Unificación:** Trata títulos y notas como eventos equivalentes de inicio de bloque.
3. **Seguridad:** Evita que el texto ordinario se filtre en la salida al actuar como un filtro de exclusión mutua (Mutex).

.. note::
   La separación real del contenido no ocurre aquí, sino en la función seguidora ``group_refs_blocks``, que consume el bloque basándose en la indentación.