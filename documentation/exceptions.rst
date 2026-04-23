========================================
Diseño de Excepciones: Jerarquía Técnica
========================================

:Módulo: exceptions.py (Nueva creación)
:Arquitectura: Basada en clases de error personalizadas
:Objetivo: Gestión de errores en Fase 3

Clases Propuestas
=================

1. **RSTStructureError**: 
   * **Descripción**: Se dispara cuando un bloque no cumple con la indentación esperada tras un punto de ruptura.
   * **Contexto**: Crucial para la nueva lógica de ``group_refs_blocks``[cite: 2, 4].

2. **RefExtractionError**:
   * **Descripción**: Error específico cuando el vigía ``is_structural_break`` detecta un inicio pero el cuerpo está vacío o mal formado[cite: 3, 12].

3. **PathValidationError**:
   * **Descripción**: Se dispara si la ruta de exportación (como ``/tmp/findOut``) no es accesible o no se puede crear.