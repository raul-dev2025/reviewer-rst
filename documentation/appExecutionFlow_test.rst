============================================
Implementación de Pruebas de Integración
============================================

Se ha incorporado el módulo ``tests_integration.py`` para asegurar la estabilidad del flujo completo de trabajo, desde la entrada por línea de comandos hasta la persistencia en disco.

Funcionalidad del Test
----------------------

El script de pruebas realiza una simulación controlada del sistema mediante los siguientes mecanismos:

* **Simulación de Entorno (Mocking)**:
    * Utiliza ``unittest.mock.patch`` para interceptar ``sys.argv``, simulando una ejecución con el flag ``--seek-refs``.
    * Intercepta ``file_manager.read_file`` para inyectar contenido rST de prueba sin depender de archivos físicos en el repositorio.
* **Gestión de Ciclo de Vida**:
    * El método ``setUp`` garantiza un entorno limpio en ``/tmp/findOut``, creando el directorio si es necesario y eliminando residuos de ejecuciones previas.
* **Validación de Resultados**:
    * Verifica la existencia física del archivo de salida ``referencias.rst``.
    * Analiza el contenido generado para asegurar que se mantienen las etiquetas críticas (ej. ``[#f1]``, ``f5``) y la estructura de la sección.

Flujo de Ejecución Verificado
-----------------------------

1. **Inicialización**: Se invoca ``main()``, lo que dispara internamente ``linker.bind_dependencies()``.
2. **Carga**: Se lee el contenido "dummy" simulado.
3. **Procesamiento**: El motor identifica las líneas que coinciden con los patrones de notas al pie.
4. **Persistencia**: Se escribe el resultado en la ruta configurada, validando que el sistema de archivos responde correctamente.

Esta suite es fundamental para detectar regresiones tras las recientes refactorizaciones del espacio de nombres y la lógica de inyección de dependencias.