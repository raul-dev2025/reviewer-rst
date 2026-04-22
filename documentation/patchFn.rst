============================================================
Procedimiento de Integración Quirúrgica de Funciones Python
============================================================

:Fecha: 2026-04-22
:Autor: Sistema de Gestión de Infraestructura
:Herramientas: GNU Patch, GNU Diff
:Estado: Consolidado

Introducción
============

Este documento describe el protocolo utilizado para la sustitución atómica de una función, en un archivo de código fuente. El objetivo es integrar cambios de colaboradores externos, garantizando la preservación de la sangría y el contexto del archivo original.

Consideraciones Previas
=======================

El uso de ``git apply`` puede resultar demasiado estricto cuando las coordenadas de línea en el parche no coinciden con el archivo de destino. Por ello, se opta por el uso de **GNU Patch**, que permite el uso de *fuzzing* para localizar el bloque de código por contexto.



Pasos del Procedimiento
=======================

1. Extracción de Referencia
---------------------------

Primero, se debe asegurar que se tiene una copia fiel de la función tal como existe actualmente en el archivo de producción. Esta se almacena en un archivo temporal para servir como base del diferencial.

.. note::

   Extraer la función actual a un archivo de referencia; ``fn_name.old``.
   Copiar y pegar la funcion en el archivo.


2. Generación del Parche de Contexto
------------------------------------

Se utiliza ``diff`` con formato unificado (``-u``) para crear la "huella digital" del cambio. Se aplican etiquetas (``--label``) para forzar al parche a referenciar el archivo de destino correcto.

.. code-block:: bash

   diff -u --label soure_file_name --label soure_file_name \
      fn_name.old \
      fn_name.new > fn_name.patch

*Nota: Este comando genera un parche que describe la transición entre la nueva lógica y la antigua.*

3. Aplicación Mediante GNU Patch
--------------------------------

La aplicación se realiza de forma resiliente. Si el parche se detecta como "invertido" (debido al orden de los archivos en el comando ``diff``), ``patch`` solicitará confirmación para aplicar el cambio en modo reverso (``-R``).

.. code-block:: bash

   patch -l --fuzz=3 soure_file_name fn_name.patch

Parámetros utilizados:
    * ``-l``: Ignora variaciones en los espacios en blanco (útil para corregir sangrías).
    * ``--fuzz=3``: Permite que el algoritmo busque el bloque de texto en posiciones distintas a las indicadas en el encabezado del parche.



Validación Resultante
=====================

Una vez aplicado, el sistema debe verificar la integración mediante el historial de control de versiones:

.. code-block:: bash

   git diff soure_file_name

La salida debe mostrar exclusivamente la sustitución de la lógica antigua por la nueva, manteniendo los encabezados (``imports``) y las funciones adyacentes totalmente intactas.

Referencias de Infraestructura
==============================

* **Manuales Consultados:** GNU Patch 2.7.6 (Larry Wall)