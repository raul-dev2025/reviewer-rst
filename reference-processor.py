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
  import os

  context_lines = []
  if not context_input:
    #
    default_path = "/tmp/findOut/input_docs.md"
    if os.path.exists(default_path):
      try:
        with open(default_path, 'r', encoding='utf-8') as f:
          lines = f.readlines()
          for line in lines:
            context_input.append(line)
      execpt Exception as e:
        print(f"️⚠️ No se pudo leer el archivo de contexto: {e}")
        return context_lines
  else:
    lines_to_process = context_input

  #  Procesado de las lineas de contexto recibido
  for line in context_input:
    striped_line = line.rstrip()
    if striped_line not in context_lines:
      context_lines.append(striped_line)

  if context_lines and not context_lines[-1].endswith('\n'):
    context_lines[-1] += '\n'

  return context_lines

def format_references(all_refs, rst_format=False):

