==========================================
Función: ``export_refs_to_out_files()``
==========================================

Documentación de Funciones de Persistencia
------------------------------------------

.. default-role:: code

Se ha implementado la capacidad de exportación física para los bloques de referencias procesados, asegurando la trazabilidad de los datos extraídos.

Función: `export_refs_to_out_files()`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Propósito**
  Toma la estructura de datos generada por el procesador y crea archivos físicos independientes para cada bloque de referencias detectado.

**Ubicación**
  `file_manager.py`

**Especificaciones Técnicas**
  * **Ruta de salida**: `/tmp/finOut`
  * **Gestión de directorios**: Utiliza `os.makedirs` con el flag `exist_ok` implícito en la lógica de control para garantizar que la ruta de destino esté disponible antes de la escritura.
  * **Nomenclatura**: Los archivos se generan bajo el patrón `out{n}.md`, donde `n` es el índice del bloque comenzando en 1.

**Parámetros de Entrada**
  * `all_blocks` (list[list[str]]): Una lista de listas, donde cada sub-lista representa un bloque completo de líneas de referencia.

**Flujo de Ejecución**
  1. Identificación del directorio de salida.
  2. Iteración numerada sobre el conjunto de bloques.
  3. Apertura de archivo con codificación `utf-8`.
  4. Volcado de contenido mediante el método `writelines(block)` para preservar la estructura original.
  5. Notificación por consola de la ruta del archivo generado.

Notas de Implementación
-----------------------

.. note::
   La función utiliza la librería estándar `os` para la manipulación de rutas y directorios, manteniendo la compatibilidad entre entornos.

.. important::
   Se ha eliminado la dependencia de lógica de previsualización de líneas, delegando la integridad estructural exclusivamente al flujo de bloques procesados.