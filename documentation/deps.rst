=========================================
Documentación Técnica: Inyección de Deps
=========================================

:Rama: ``refactor/centralized-imports``
:Estado: Implementado y Validado
:Descripción: Centralización de dependencias y resolución de importaciones circulares.

Introducción
============

Para mejorar la mantenibilidad y evitar dependencias circulares entre los módulos de procesamiento de rST (como ``processor.py``, ``cleaner.py`` y ``formatter.py``), se ha implementado un patrón de inyección de dependencias mediante un componente orquestador denominado ``linker.py``.

Arquitectura del Linker
=======================

El archivo ``linker.py`` actúa como el nexo de unión del sistema. Su función principal es inyectar objetos, librerías estándar y constantes en los espacios de nombres (*namespaces*) de los submódulos en tiempo de ejecución.

Funcionamiento del Enlace
-------------------------

1. **Definición de Dependencias**: El linker importa todos los componentes necesarios (incluyendo librerías como ``re`` y constantes de ``regex.py``).
2. **Inyección de Atributos**: Mediante la función ``bind_dependencies()``, se asignan estos objetos directamente a los módulos cargados.

.. code-block:: python

   # Ejemplo de inyección en linker.py
   cleaner.re = re
   cleaner.PANDOC_LINK_PATTERN = regex.PANDOC_LINK_PATTERN

Implementación en Submódulos
============================

Para que los submódulos puedan consumir estas dependencias inyectadas sin generar errores de ámbito (*NameError*), deben referenciarlas a través de su propio nombre de módulo.

Ejemplo en ``cleaner.py``:

.. code-block:: python

   import cleaner
   import re

   def clean_line_content(line):
       # Acceso a la variable inyectada por el linker
       return re.sub(cleaner.PANDOC_LINK_PATTERN, r'\1', line)

Protocolo de Inicialización
===========================

Es imperativo que el linker sea invocado antes de cualquier lógica de procesamiento para garantizar que los "cables" estén conectados.

Entorno de Producción
---------------------
En ``review.py``, la inicialización se realiza en el punto de entrada:

.. code-block:: python

   def main():
       linker.bind_dependencies()
       # ... lógica de la aplicación

Entorno de Pruebas (Unittest)
----------------------------
Para las pruebas unitarias en ``test_rst.py``, se utiliza el gancho ``setUpClass`` para asegurar una única inyección antes de ejecutar la batería de tests:

.. code-block:: python

   @classmethod
   def setUpClass(cls):
       linker.bind_dependencies()

Beneficios de la Rama
=====================

- **Zero-Footprint Circular**: Se eliminan las importaciones cruzadas entre procesadores.
- **Configuración Centralizada**: Los cambios en patrones de expresiones regulares en ``regex.py`` se propagan automáticamente a través del linker.
- **Aislamiento**: Los submódulos permanecen ligeros y enfocados exclusivamente en su lógica de transformación de texto.