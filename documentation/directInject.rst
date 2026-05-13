====================================================
Nota Técnica: Inyección Directa de Dependencias
====================================================

:Fecha: 2026-05-11
:Autor: Linker System
:Estado: Implementado (Opción A)

Contexto
========

Para mantener el principio de **Zero-Footprint**, se ha evitado que los submódulos (como ``reference_processor.py``) realicen importaciones de lógica de negocio o de sistema. En su lugar, el orquestador (``linker.py``) "inyecta" las piezas necesarias durante la fase de vinculación.

Mecánica de Inyección Directa
=============================

A diferencia de la delegación (donde el módulo llama al linker para pedir una función), la **inyección directa** crea un enlace en el espacio de nombres local del submódulo.

Configuración en ``linker.py``
------------------------------

En la función ``bind_dependencies()``, se realiza la asignación cruzada:

.. code-block:: python

    # El linker toma la función de file_manager y la coloca en reference_processor
    reference_processor.prepare_file = file_manager.prepare_file

Uso en ``reference_processor.py``
---------------------------------

El submódulo solo necesita declarar el puntero inicial para evitar errores de linting, y luego invoca la función de forma nativa:

.. code-block:: python

    prepare_file = None  # Puntero inyectado

    def group_refs_blocks(lines):
        # ... lógica ...
        prepare_file(all_ref_blocks)  # Llamada directa y limpia


Inyección y Gestión de Scopes
=============================

Para que la inyección externa sea posible, los submódulos deben exponer un "punto de anclaje" en su espacio de nombres de módulo.

¿Por qué declaración Global (Nivel de Módulo) y no Local?
--------------------------------------------------------

1. **Accesibilidad del Orquestador**: El ``linker.py`` opera sobre el objeto módulo (p.ej. ``reference_processor``). Solo puede inyectar atributos que residan en el namespace del módulo. Las variables locales a una función son invisibles para el Linker.
2. **Placeholder de Compilación**: Al declarar ``prepare_file = None`` a nivel de módulo, se informa al intérprete de Python que el símbolo existe. Esto evita un ``NameError`` cuando las funciones internas intentan invocarlo antes de que el valor real sea asignado.
3. **Persistencia del Estado**: Una vez que ``bind_dependencies()`` sustituye el ``None`` por la función real de ``file_manager``, ese puntero queda disponible para todas las funciones del módulo de forma persistente.

Implementación en ``reference_processor.py``
---------------------------------------------

.. code-block:: python

    # Ámbito de Módulo: Actúa como 'cerradura' para la inyección
    prepare_file = None  
    this = None

    def group_refs_blocks(lines):
        # ... lógica de la máquina de estados ...
        
        # Invocación directa: La función ya reside en el namespace local
        if prepare_file:
            prepare_file(all_ref_blocks)

Conclusión Técnica
==================

Este enfoque transforma los submódulos en estructuras pasivas que reciben sus capacidades del orquestador. La declaración global de los punteros es el mecanismo técnico que permite este desacoplamiento, garantizando que el módulo sea importable sin dependencias, pero funcional tras la vinculación.


Discusión Técnica
=================

Ventajas de la Opción A
-----------------------

1. **Simplificación de Llamadas**: Elimina la necesidad de prefijos como ``linker.prepare_file()`` o ``this.prepare_file()``. La función reside, para efectos prácticos, dentro del módulo.
2. **Desacoplamiento Total**: ``reference_processor`` no sabe que la función proviene de ``file_manager``. Solo requiere que la firma de la función (parámetros) se respete.
3. **Mantenibilidad**: Si en el futuro decidimos que la preparación de archivos la haga otro módulo distinto a ``file_manager``, solo debemos cambiar una línea en el ``linker.py``.

Consideraciones de Integridad
-----------------------------

Esta técnica requiere que la inyección ocurra *antes* de cualquier ejecución lógica. Por ello, el archivo de test (``test_rst.py``) invoca siempre ``linker.bind_dependencies()`` en el ``setUpClass``.