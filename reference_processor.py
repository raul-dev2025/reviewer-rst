# -*- coding: utf-8 -*-

import os, re


this = None

def group_refs_blocks(lines):
    """
    Maquina de estado para capturar bloques de referencias.
    Captura bloques de referencias con integridad estructural.
    """

    all_ref_blocks = []
    current_block = []
    in_reference_block = False

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

    prepare_file(all_ref_blocks)

    return all_ref_blocks

def extract_references_context(context_input):
  """
  Extrae el contexto para las referencias desde el texto del documento.
  Busca la referencia en el texto y las dos palabras previas como contexto.
  """
  context_lines = []


  if context_input:
    full_text = ' '.join(context_input) if isinstance(context_input, list) else context_input
    matches = list(reference_pattern.finditer(full_text))

    for match in matches:
      start_idx = match.start()
      reference_text = match.group().strip()

      # texto previo de la referencia
      preceding_text = full_text[:start_idx].strip()

      words = preceding_text.split()

      if len(words) == 0:
        context_snippet = "seccion de referencias"
      elif len(words) >= 2:
        context_snippet = " ".join(words[-2:])
      else:
        context_snippet = words[0]

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
    if isinstance(ref, dict):
      ref_val = ref.get('reference', '')
    else:
      ref_val = str(ref)

    clean_ref = ref_val.strip('[]').strip()

    if rst_format:
      formatted_output.append(f"..  [{clean_ref}]")
    else:
      formatted_output.append(f"- {clean_ref}")



  return "\n".join(formatted_output)

