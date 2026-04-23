============================================================
Hoja de Ruta: Transición a Arquitectura Modular (rST)
============================================================

:Proyecto: Reviewer-RST
:Responsable: Raúl Vílchez & Gemini
:Estado: Fase de Planificación Post-Test

Este documento detalla los pasos necesarios para desmantelar la función monolítica ``join_broken_paragraphs()`` y sustituirla por el nuevo sistema de procesamiento en tres fases, garantizando la estabilidad de la aplicación.

Fases de la Transición
======================

1. Auditoría de Referencias Cruzadas
------------------------------------
* **Tarea**: Localizar mediante herramientas de búsqueda (grep/IDE) todas las menciones a la función antigua en el paquete de scripts.
* **Objetivo**: Evitar errores de tipo ``NameError`` durante la ejecución.

2. Refactorización de la Suite de Tests
---------------------------------------
* **Tarea**: Editar ``test_rst.py`` para eliminar las pruebas que invocan directamente a la función suprimida.
* **Tarea**: Asegurar que los tests de las tres nuevas sub-funciones (Partes 1, 2 y 3) cubren todos los casos de uso previos. Es decir, replicar los test obsoletos en las nuevas funciones.
* **Objetivo**: Mantener una maquinaria de depuración limpia y sin falsos negativos.

3. Orquestación en el Módulo Principal (review.py)
--------------------------------------------------
* **Tarea**: Modificar el punto de entrada de procesamiento en ``review.py``.
* **Lógica a Implementar**:
    1. Obtención de títulos (``get_document_titles``).
    2. Agrupación estructural (``group_lines_into_raw_blocks``).
    3. Filtrado y refinado final (``filter_and_format_blocks``).
* **Objetivo**: Integrar la nueva lógica en el flujo de trabajo real del script.

4. Verificación de Integración Final
------------------------------------
* **Tarea**: Ejecutar el script sobre un archivo rST real y verificar que el resultado es idéntico o superior al método anterior.
* **Objetivo**: Confirmación final de éxito.

.. code-block:: python

   def join_broken_paragraphs(lines):
      if not lines:
         return []

      1. Identificar todos los títulos del documento para la heurística del TOC
      Filtramos líneas que son títulos usando is_structural_break
      doc_titles = []
      for i, L in enumerate(lines):
         nxt = lines[i+1] if i+1 < len(lines) else None
         if is_structural_break(L.strip(), next_line=nxt):
               Si es un título subrayado, el texto está en L
               if nxt and is_underline(nxt):
                  doc_titles.append(L.strip())

      blocks = []
      Insertamos la directiva TOC oficial al inicio
      blocks.extend(get_toc_directive())
      
      current_block = []
      first_text_block_processed = False

      for i in range(len(lines)):
         line = lines[i].strip()
         
         if not line:
               if current_block and i + 1 < len(lines):
                  if is_likely_same_paragraph(current_block[-1], lines[i+1].strip()):
                     continue
               
               if current_block:
                  text_content = " ".join(current_block)
                  
                  Heurística de limpieza de TOC residual
                  if not first_text_block_processed:
                     if is_legacy_toc(text_content, doc_titles):
                           current_block = []
                           first_text_block_processed = True
                           continue
                  
                  blocks.append(text_content)
                  first_text_block_processed = True
                  current_block = []
               continue

         Lógica de detección estructural (Títulos/Bloques)
         next_l = lines[i+1] if i+1 < len(lines) else None
         if is_structural_break(line, next_line=next_l):
               if current_block:
                  blocks.append(" ".join(current_block))
                  current_block = []
               blocks.append(line)
         else:
               current_block.append(line)

      if current_block:
         blocks.append(" ".join(current_block))

      return blocks


