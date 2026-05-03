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
                elif next_line.strip().startswith("-") and len(next_line.strip()) >= 3:
                  break
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
  Extrae el contexto para las referencias desde el texto del documento.
  Busca la referencia en el texto y las dos palabras previas como contexto.
  """
  import re

  context_lines = []


  if context_input:
    full_text = ''.join(context_input) if isinstance(context_input, list) else context_input
    matches = list(re.finditer(r'(?:^|\s+)(?:\[#?[a-zA-Z0-9]+\]|`[^`]+<#?[a-zA-Z0-9]+>`__|\(?[a-zA-Z0-9]+\)?)', full_text))
    # buscamos un  mecanismo que guarde el contexto

    for match in matches:
      start_idx = match.start()
      reference_text = match.group().strip()

      # texto previo de la referencia
      preceding_text = full_text[:start_idx].strip()

      words = preceding_text.split()
      if len(words) >= 2:
        context_snippet = " ".join(words[-2:])
      elif len(words) == 1:
        context_snippet = words[0]
      else:
        context_snippet = "indent[3]"

      # Filtra, y guarda el cxt asociado a la ref.
      if reference_text:
        context_lines.append({
        "reference": reference_text,
        "context": context_snippet
        })


  return context_lines

def format_references(all_refs, rst_format=False):
  """
  Da formato rST a las referencias encontradas en el documento.
  """
  if not all_refs:
    return  ""

  formatted_output = []

  for ref in all_refs:
    if rst_format:
      match = re.search(r'(?:#?[a-zA-Z0-9]+|`[^`]+<#?[a-zA-Z0-9]+>`__)', ref)
      clean_ref = match.group(0) if match else ref.strip('[]')
      formatted_output.append(f"..  [{clean_ref}]")
    else:
      formatted_output.append(f"- {ref}")



  return "\n".join(formatted_output)

