============================================================
Mecanismo de Normalización Semántica mediante Clausuras (.rst)
============================================================

.. section-author:: Raul Vilchez
.. date:: May 2026

Introducción
============

Para resolver la inconsistencia sintáctica de las referencias cruzadas heredadas de conversiones previas (como restos de Pandoc o sintaxis explícitas de Markdown) sin acoplar lógica rígida (*hardcoding*) en el formateador pasivo, se ha diseñado e implementado una arquitectura desacoplada basada en **clausuras dinámicas conducidas por datos**.

El formateador final (``format_references()``) actúa de forma puramente pasiva y agnóstica, delegando la responsabilidad de la homogeneización textual en un motor de sustitución gobernado por el archivo de configuración ``archivo_regex.txt``.

Arquitectura del Motor
======================

El pipeline de procesamiento se divide en tres fases bien diferenciadas:

1. **Carga y Compilación Dinámica:** El módulo ``closures.py`` lee las reglas desde ``archivo_regex.txt`` en tiempo de ejecución. Cada línea se parsea de forma posicional pura utilizando espacios en blanco mediante el método ``line.split(None, 3)``.
2. **Asignación Posicional Estricta:** La estructura de cada regla se descompone directamente en tres componentes secuenciales obligatorios:
   
   .. code-block:: python

      patron, busqueda, reemplazo = line.split(None, 3)

3. **Generación de Clausuras (Closures):** Por cada regla válida, se genera y compila una función anidada que encapsula de manera aislada el patrón de búsqueda y su correspondiente patrón de sustitución (manteniendo el estado de sus variables locales de ámbito).
4. **Pipeline Secuencial:** El texto pasa de manera ordenada a través de la cadena de clausuras compiladas, transformando las anomalías en llamadas normalizadas listas para rST de forma transparente.

Especificación de Reglas Activas (archivo_regex.txt)
===================================================

El archivo de configuración utiliza expresiones regulares estrictas divididas por espacio posicional (``patron busqueda reemplazo``). El conjunto actual de reglas que garantiza el éxito del pipeline es el siguiente:

.. code-block:: text

   # Regla 1: Limpia y unifica los índices viejos/remanentes de Markdown heredados de Pandoc
   `([^<]+)<#[^>]+>`__? `([^<]+)<#[^>]+>`__? \1

   # Regla 2: Unifica las referencias que ya vienen entre corchetes en el cuerpo del texto (ej. [1] o [i1])
   \[(#?[a-zA-Z]*\d+)\] \[(#?[a-zA-Z]*\d+)\] [\1]_

   # Regla 3: Detecta literales numéricos sueltos (ej: i1 o f5) que actúan como llamadas implícitas
   \b[a-zA-Z]\d+\b(?!\s*<) \b([a-zA-Z])(\d+)\b [\1\2]_

   # Regla 4: Intercepta literales puros al final de frase en contextos específicos (ej: f5.)
   \b([a-zA-Z])(\d+)\b\. \b([a-zA-Z])(\d+)\b\. [\1\2]_.

Flujo de Transformación de Datos
================================

A continuación se muestra el ciclo de vida de los datos desde su entrada cruda hasta su preparación final para la directiva destino:

+--------------------------+-----------------------+---------------------------------+
| Entrada Cruda            | Salida Motor Closures | Destino Final (format_refs)     |
+==========================+=======================+=================================+
| ``[#f2]``                | ``[#f2]_``            | ``.. [#f2]``                    |
+--------------------------+-----------------------+---------------------------------+
| `` `f3 <#f3>`_ ``        | ``[f3]_``             | ``.. [f3]``                     |
+--------------------------+-----------------------+---------------------------------+
| ``f5.`` (en texto)       | ``[f5]_.``            | ``.. [f5]``                     |
+--------------------------+-----------------------+---------------------------------+

Ventajas del Diseño
===================

* **Desacoplamiento total:** ``reference_processor.py`` no conoce expresiones regulares ni nombres de variables concretas (``f2``, ``z33``).
* **Mantenibilidad:** La adición de soporte para nuevos formatos no requiere reescribir ni compilar código fuente, basta con añadir una línea declarativa al archivo de configuración respetando la separación posicional de sus componentes.