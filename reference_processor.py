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
        stripped = line.strip()

        # La linea vacia rompe contexto de referencia
        if not stripped:
          if current_block:
            all_ref_blocks.append(current_block)
            current_block = []
          in_reference_block = False
          i += 1
          continue

        if this.is_structural_break(line, True):
          if current_block:
            all_ref_blocks.append(current_block)

          current_block = [line]
          in_reference_block = True
          i += 1
          continue

        # Valida cuerpo del bloque
        if in_reference_block:
          # Si esta indentada
          if line.startswith(' ') or line.startswith('t'):
            current_block.append(line)
          else:
            # Si no esta indentada
            if not (stripped.startswith(".. [") or stripped.startswith("[") or stripped.startswith(":")):
              all_ref_blocks.append(current_block)
              current_block = []
              in_reference_block = False
              continue

            if this.is_underline(line):
              all_ref_blocks.append(current_block)
              current_block = []
              in_reference_block = False
              continue

            raise StructuralIntegrityError(i + 1, "Falta indentación en bloque de referencia")

            all_ref_blocks.append(current_block)
            current_block = []
            in_reference_block = False
            # No incrementamos i para re-evaluar la linea como inicio
            continue

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

