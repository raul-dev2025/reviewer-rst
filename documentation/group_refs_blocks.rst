======================================
Documentación Técnica: group_refs_blocks
======================================

:Módulo: processor.py
:Función: group_refs_blocks
:Tipo: Máquina de Estados / Agrupador
:Fase: Fase 3 - Integración Estructural

Descripción
===========

Esta función implementa una máquina de estados encargada de segmentar el flujo de líneas del documento en bloques discretos de referencias. Su objetivo es garantizar la integridad de cada entrada bibliográfica o sección de recursos, evitando la fragmentación innecesaria.

Estructuras de Datos Principales
================================

La función gestiona la persistencia de los datos mediante dos vectores principales:

* **current_block**: Actúa como un acumulador de líneas. Almacena temporalmente el contenido del bloque que se está analizando en el momento actual, basándose en los puntos de ruptura detectados.
* **all_ref_blocks**: Es el contenedor global. Representa la suma de todos los bloques capturados y validados durante la ejecución del proceso.

Lógica de Control y Estados
===========================

Puntos de Ruptura (Disparadores)
-------------------------------

El primer condicional de la función invoca a ``is_structural_break(line, seek_refs=True)``. Esta comprobación es crítica por dos motivos:

1. **Validación de Modo**: Asegura que la detección de rupturas opere estrictamente bajo el flag ``seek_refs``, ignorando estructuras que no sean relevantes para la fase de extracción de referencias.
2. **Cierre de Bloque**: Si se detecta un nuevo punto de ruptura y existe contenido en ``current_block``, el sistema interpreta que el bloque anterior ha finalizado, lo traslada a ``all_ref_blocks`` y comienza una nueva acumulación.

Cierre de Seguridad y Persistencia
----------------------------------

El segundo condicional relevante se encuentra tras la finalización del bucle principal de lectura:

* **Vaciado Final**: Comprueba si ``current_block`` contiene datos residuales. Esto ocurre cuando el último bloque analizado llega al final del archivo sin encontrar un nuevo punto de ruptura que dispare su guardado.
* **Consolidación**: Garantiza que el último bloque capturado se integre correctamente en ``all_ref_blocks`` antes de retornar el resultado.

Mecánica de Filtrado (is_note / is_other_header)
------------------------------------------------

Dentro del estado de acumulación, la función aplica filtros adicionales para segmentar bloques que, aunque no son rupturas estructurales mayores, requieren independencia:

* **Notas**: Identifica la palabra clave "Nota" (y sus variantes) para separar aclaraciones del cuerpo de la referencia.
* **Cabeceras (#)**: Evita que títulos de menor jerarquía se mezclen con el contenido bibliográfico, manteniendo la limpieza visual de la exportación.

.. note::
   Esta función es la responsable directa de evitar la creación de múltiples archivos basura, al tratar de agrupar líneas relacionadas en una única entidad lógica antes de la persistencia en disco.

-----

Análisis de Validación: group_refs_blocks.patch
================================================

Resumen del Cambio
------------------

El parche ``group_refs_blocks.patch`` representa una evolución crítica en la lógica de captura, transitando de un modelo de lectura lineal a una **máquina de estados con consumo por indentación**. Esta modificación es el pilar para resolver la fragmentación excesiva detectada en las fases de prueba (salidas out1.md a out130.md).

Validación de Mejoras Técnicas
==============================

1. Cohesión de Bloque (Mecánica de Salto)
-----------------------------------------

* **Antes**: Se procesaba línea a línea, lo que causaba que cada entrada de referencia se tratara como un archivo independiente.
* **Ahora**: Implementa un bucle ``while`` que permite al procesador "saltar" y capturar grupos de líneas relacionados, tratando el bloque de referencias como una entidad única, de forma análoga a los bloques de código literal (``::``).

2. Captura Quirúrgica por Indentación
-------------------------------------

Se introduce un bucle interno que garantiza la integridad del bloque si se cumplen estas condiciones:

* **Indentación**: La línea comienza con espacios o tabuladores (preservando URLs dependientes).
* **Líneas en Blanco**: Se mantienen para no romper el espaciado interno de la bibliografía.
* **Notas Adyacentes**: Captura notas pegadas a la anterior dentro del mismo bloque lógico.

3. Saneamiento del Flujo (Limpieza de Ruido)
--------------------------------------------

* **Delegación**: Se elimina el uso de patrones manuales (``nota_pattern``) y detecciones genéricas de almohadillas (``#``).
* **Impacto**: La decisión de ruptura queda delegada exclusivamente a ``is_structural_break(..., seek_refs=True)``, evitando que menciones casuales en el texto disparen la creación de archivos basura.

4. Gestión de Persistencia
--------------------------

El parche asegura la correcta administración de los vectores de datos:

* **Vaciado Preventivo**: Si existe contenido en ``current_block`` al detectar una nueva sección, se vuelca en ``all_ref_blocks`` antes de reiniciar.
* **Cierre de Seguridad**: Implementa un bloque ``if current_block`` final para asegurar que la última referencia del archivo no se pierda en el buffer.

Conclusión de Auditoría
=======================

El parche es **coherente** con los objetivos de la Fase 3 y soluciona la regresión de fragmentación. Se recomienda su aplicación inmediata sobre la cabecera ``024ca6c`` para consolidar la "cirugía de bloques" y proceder con el desarrollo de la gestión de excepciones.