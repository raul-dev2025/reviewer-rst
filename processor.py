# -*- coding: utf-8 -*-

import re
from cleaner import clean_line_content

def is_underline(line):
    """Detecta si una línea es un subrayado de título rST."""
    if not line: return False
    stripped = line.strip()
    return len(stripped) >= 3 and all(c == stripped[0] for c in stripped) and stripped[0] in '=-~^'

def is_potential_title_text(line):
    """Detecta si una línea de texto tiene apariencia de título."""
    if not line: return False
    stripped = line.strip()
    # Un título no es un párrafo largo ni termina en punto
    return 0 < len(stripped) < 100 and not stripped.endswith('.')

def is_structural_break(line, next_line=None):
    """Determina si la línea actual rompe la continuidad del párrafo."""
    stripped = line.strip()
    if not stripped: return True
    
    # 1. Directivas o bloques de código
    if stripped.startswith('.. ') or stripped.startswith('   :') or stripped.startswith('::'):
        return True

    # 2. Si la línea misma es un subrayado
    if is_underline(line):
        return True

    # 3. Anticipación: Si la siguiente línea es un subrayado, la actual es un título
    if next_line and is_underline(next_line):
        return True
    
    return False

def is_likely_same_paragraph(line_a, line_b):
  #
  if line_a and line_a[-1] not in '.!?':
    if line_b and line_b[0].islower():
      return True
  return False

def identify_literal_blocks(lines):
    """
    Identifica los rangos (inicio, fin) de bloques de código basándose en 
    directivas (::, .. code-block::) e indentación.
    """
    protected_ranges = []
    in_block = False
    start_index = None
    last_valid_line = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # CASO 1: Buscamos el inicio de un bloque
        if not in_block:
            if stripped == "::" or stripped.startswith(".. code-block::"):
                in_block = True
                start_index = i
                last_valid_line = i
            continue

        # CASO 2: Estamos dentro de un bloque
        # Una línea es válida si está vacía O si tiene al menos 3 espacios de indentación
        is_indented = line.startswith("   ")
        is_empty = not stripped

        if is_indented:
            last_valid_line = i
        elif is_empty:
            # Las líneas vacías se aceptan, pero no confirman el final todavía
            pass
        else:
            # Si no está indentada y no está vacía, el bloque terminó en la última línea indentada
            protected_ranges.append((start_index, last_valid_line))
            in_block = False
            # Importante: Re-evaluamos la línea actual por si fuera el inicio de OTRO bloque
            if stripped == "::" or stripped.startswith(".. code-block::"):
                in_block = True
                start_index = i
                last_valid_line = i

    # Si terminamos el archivo dentro de un bloque, lo cerramos
    if in_block:
        protected_ranges.append((start_index, last_valid_line))

    return protected_ranges

def extract_literal_blocks(lines, ranges):
    """
    Sustituye los bloques de codigo identificados por marcadores.
    Retorna lineas con marcadores y diccionario de bloques.
    """
    blocks_dict = {}
    new_lines = list(lines)

    for i, (start, end) in enumerate(reversed(ranges)):
        # Crea un ID unico para el bloque
        idx = len(ranges) - 1 - i
        block_id = f"[[CODE_BLOCK_{idx}]]"

        # Almacena  el contenido original unido por saltos de linea
        blocks_dict[block_id] = "\n".join(lines[start:end+1])

        # Reemplazamos el bloque original, por el marcador
        new_lines[start:end+1] = [block_id]
    
    return new_lines, blocks_dict

def reinject_literal_blocks(text, blocks_dict):
    """
    Busca los marcadores y los sustituye por el 
    contenido almacenado en el diccionario.
    """
    final_text = text
    for block_id, original_content in blocks_dict.items():
        #Sustituye el marcador por el codigo guardado
        final_text = final_text.replace(block_id, original_content)

    return final_text

def is_legacy_toc(block, documet_titles):
  """
  Detecta un indice residual MarkDown. Se trata de un
  bloque largo que contine los titulos de seccion.
  """
  if not documet_titles:
    return False

  coincidencias = 0
  # Limpiamos el bloque antes de empezar
  block_clean = block.lower()

  for title in documet_titles:
    if title.lower() in block_clean:
      coincidencias += 1

  return coincidencias >= 2

def get_toc_directive():
  """
  Directiva estandar para tabla de contenidos 
  """
  return [
    ".. contents:: Tabla de contenidos\n   :depth: 3",
    ""
  ]

# El maestro de ceremonias
def process_rst_blocks(lines):
  """
  Coordina la secuencia de llamadas a funcion, en el orden
  correcto y esperado. Sustituye a join_broken_paragraphs()
  """
  # 1. Logica de aplicacion; el recolector
  titles = get_document_titles(lines)

  # 2. Agrupacion estructural; el evaluador de continuidad
  raw_blocks = group_lines_into_raw_blocks(lines)

  # 3. Refinado; El filtro de bloques
  final_blocks = filter_and_format_blocks(raw_blocks, titles)

  return final_blocks

# El recolector
def get_document_titles(lines):
  """
  Busca los titulos en el documento
  Basa su logica en is_potential_title_text e is_underline.
  """
  titles = []
  for i in range(len(lines) - 1):
    current = lines[i].strip()
    next_line = lines[i+1].strip()
    if is_potential_title_text(current) and is_underline(next_line):
      titles.append(current)
  return titles

# El evaluador de continuidad
def group_lines_into_raw_blocks(lines):
  """
  Agrupa líneas en bloques lógicos.
  Cohesiona parrafos fragmentados.
  """
  from processor import is_structural_break, is_likely_same_paragraph

  raw_blocks = []
  current_acc = []

  for i in range(len(lines)):
    line = lines[i].strip()
    next_line = lines[i+1].strip() if i+1 < len(lines) else None

    if line:
      current_acc.append(line)

    # Determina si aqui termina el bloque
    should_close = False

    if not line:
      if current_acc and next_line:
        if not is_likely_same_paragraph(current_acc[-1], next_line):
          should_close = True
      elif current_acc:
        should_close = True
    elif is_structural_break(line, next_line):
      should_close = True

    if should_close and current_acc:
      raw_blocks.append(" ".join(current_acc).strip())
      current_acc = []

  if current_acc:
    raw_blocks.append(" ".join(current_acc).strip())

  return raw_blocks

def group_refs_blocks(lines):
  """
  Maquina de estado para capturar bloques de referencias.
  """
  # Patrón que busca:
  # ^\s* -> Posibles espacios al inicio
  # (\*\*|__)?    -> Opcionalmente negritas (Markdown: ** o __)
  # [Nn]ota       -> La palabra "nota" (mayúscula o minúscula)
  # (?:[ \t]+de)? -> Opcionalmente " de" (sin capturarlo)
  # .* -> Cualquier cosa después
  nota_pattern = re.compile(r'^\s*(\*\*|__)?nota(?:[ \t]+de)?', re.IGNORECASE)

  all_ref_blocks = []
  current_block = []

  for line in lines:
    is_ref_start = is_structural_break(line, seek_refs=True)

    if is_ref_start:
      if current_block:
        all_ref_blocks.append(current_block)

      current_block = [line]
      continue

    if current_block:
      is_note = bool(nota_pattern.match(line.strip()))      
      is_other_header = line.startswith('#')

      if is_note or is_other_header:
        all_ref_blocks.append(current_block)
        current_block = []
      else:
        current_block.append(line)

  if current_block:
    all_ref_blocks.append(current_block)

  return all_ref_blocks

# El filtro de bloques
def filter_and_format_blocks(raw_blocks, doc_titles):
  """
  Limpia, filtra y añade la directiva rST (TOC).
  """
  from cleaner import clean_line_content

  blocks = []
  # Subimos la directiva TOC, al almacen de bloques
  blocks.extend(get_toc_directive())

  for rb in raw_blocks:
    # Limpiamos lo que no pudo Pandoc
    clean_text = clean_line_content(rb)

    # comprueba si es el indice .md
    if is_legacy_toc(clean_text, doc_titles):
      continue

    # Despues de limpiar, guardamos si hay contenido
    if clean_text:
      blocks.append(clean_text)

  return blocks











