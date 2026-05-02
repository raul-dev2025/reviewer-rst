# -*- coding: utf-8 -*-

import os

def group_refs_blocks(lines):
    """
    Maquina de estado para capturar bloques de referencias.
    Captura bloques de referencias con integridad estructural (estilo bloque de código).
    """
    from  processor import is_structural_break
    from exceptions import StructuralIntegrityError
    all_ref_blocks = []
    current_block = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # ¿Es el inicio de una sección de referencias o una nota?
        if is_structural_break(line, seek_refs=True):
            if current_block:
                all_ref_blocks.append(current_block)

            # Iniciamos el nuevo bloque con la línea disparadora
            current_block = [line]
            i += 1

            # Consumimos el "cuerpo" del bloque (líneas indentadas)
            while i < len(lines):
                next_line = lines[i]

                # Si la línea está indentada, es parte del bloque (como las URLs de tu out130)
                if next_line.startswith(' ') or next_line.startswith('\t') or not next_line.strip():
                  current_block.append(next_line)
                  i += 1
                # Si viene otra nota pegada, también es parte del mismo bloque lógico
                elif is_structural_break(next_line, seek_refs=True):
                  current_block.append(next_line)
                  i += 1
                else:
                  if not next_line.strip().startswith(".. [") and not next_line.strip().startswith(":"):
                    raise StructuralIntegrityError(i + 1, "Falta indentación en bloque de referencia")
                  # Encontramos texto sin indentar: fin del bloque quirúrgico
                  break
            continue # Volvemos al bucle principal con el índice actualizado

        i += 1

    if current_block:
        all_ref_blocks.append(current_block)

    return all_ref_blocks

def extract_references_context(context_input):
  """
  Extrae el contexto para las referencias desde el documento original.
  """

  context_lines = []


  return context_lines

def format_references(all_refs, rst_format=False):

