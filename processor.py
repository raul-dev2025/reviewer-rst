# -*- coding: utf-8 -*-
# Copyright (c) 2026 Raúl Vílchez Ruiz <r4u1974@gmail.com>
# Distributed under the terms of the MIT License.
# See LICENSE file in the project root for full license information.

this = None

def is_underline(line):
    """Detecta si una línea es un subrayado de título rST."""
    if not line: return False
    stripped = line.strip()
    return bool(this.RST_UNDERLINE_PATTERN.match(stripped))

def is_potential_title_text(line):
    """Detecta si una línea de texto tiene apariencia de título."""
    if not line: return False
    stripped = line.strip()
    # Un título no es un párrafo largo ni termina en punto
    return 0 < len(stripped) < 100 and not stripped.endswith('.')

def is_structural_break(line, seek_refs=False):
  """
  Determinar si la línea actual representa un punto de ruptura.
  """
  stripped = line.strip()
  if not stripped:
    return True

  if stripped.startswith('.. ') or stripped.startswith('::'):
    return True

  if stripped.startswith(':'):
    return True

  if stripped.startswith('   :'):
    return True

  if seek_refs:
    is_title = this.ADMIN_SECTION_PATTERN.match(stripped)
    is_footnote = this.FOOTNOTE_PATTERN.match(stripped)

    return bool(is_title or is_footnote)

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

def is_legacy_toc(clean_text, doc_titles):
    """
    Determina si un bloque corresponde a un antiguo índice manual (TOC residual)
    saneando temporalmente la línea para identificar los 6 escenarios de Pandoc.
    """
    if not clean_text or not doc_titles:
        return False

    text_stripped = clean_text.strip()
    text_base = this.re.sub(this.TOC_LIST_PREFIX_PATTERN, '', text_stripped)
    text_base = this.re.sub(this.TOC_ANCHOR_REMOVE_PATTERN, '', text_base).strip()

    if not text_base:
        return False

    clean_titles_set = set()
    for title in doc_titles:
        t_base = this.re.sub(this.TOC_ANCHOR_REMOVE_PATTERN, '', title).strip()
        if t_base:
            clean_titles_set.add(t_base)

    # Coincidencia directa con titulo real (COMENTADO / ELIMINADO)
    # if text_base in clean_titles_set:
    #   return True

    words_found = 0
    for base_title in clean_titles_set:
        if base_title in text_base:
            words_found += 1

    if words_found >= 2:
        return True

    if len(this.re.findall(this.TOC_ANCHOR_REMOVE_PATTERN, clean_text)) >= 2:
        return True

    return False

def get_toc_directive():
  """
  Directiva estandar para tabla de contenidos 
  """
  toc_lines = (
    ".. contents:: Tabla de contenidos\n"
    "   :local:\n"
    "   :backlinks: none\n"
    "   :depth: 2\n"
    ""
  )
  return [toc_lines, ""]

def validate_structural_integrity(lines):
    """
    Valida la integridad estructural en los bloques de referencias.
    MOTIVO DEL CAMBIO: Se aísla la validación de la indentación para que pueda
    ser ejecutada independientemente del flujo, evitando acoplar la responsabilidad
    al modo seek_refs o a la agrupación de bloques.
    """
    in_reference_block = False
    has_reference = False
    for i, line in enumerate(lines):
        stripped = line.strip()

        # Busca el patron que inyecta el linker
        footnote_patt = getattr(this, 'FOOTNOTE_PATTERN', None)

        is_start_of_ref = stripped.startswith(".. [") and "]" in stripped
        is_footnote = footnote_patt.match(stripped) if footnote_patt else False

        is_hybrid_ref = "<#" in stripped or "[#f" in stripped

        if not stripped:
          in_reference_block = False
          continue

        if is_start_of_ref or is_footnote or is_hybrid_ref:
          if is_start_of_ref or is_footnote:
            in_reference_block = True
          has_reference = True

        if in_reference_block:
          is_indented = line.startswith(" ") or line.startswith("\t")

          if not is_indented:
            if not stripped.startswith(".. [") and not stripped.startswith(":"):
              if is_potential_title_text(line) or len(stripped) > 0:
                in_reference_block = False
              else:
                raise this.StructuralIntegrityError(i + 1, "Falta indentación en bloque de referencia")
            else:
              in_reference_block = False

    return has_reference

# El maestro de ceremonias
def process_rst_blocks(lines, seek_refs=False):
  """
  Coordina la secuencia de llamadas a funcion, en el orden
  correcto y esperado.
  """
  has_refs = validate_structural_integrity(lines)

  if not seek_refs and has_refs:
    base_dir = this.os.path.dirname(this.os.path.abspath(__file__))
    resource_path = this.os.path.join(base_dir, "warnings.rst")
    if this.os.path.exists(resource_path):
      msg = getattr(this, 'read_file', lambda p: "")(resource_path)
      if msg:
        print(msg)

  raw_blocks = group_lines_into_raw_blocks(lines, seek_refs=seek_refs)

  if seek_refs:
    # Evita pasar el filtro rST.
    return raw_blocks
    
  # Flujo estandar
  titles = get_document_titles(lines)
  final_blocks = filter_and_format_blocks(raw_blocks, titles, seek_refs=seek_refs)

  return final_blocks

# El recolector
def get_document_titles(lines):
  """
  Busca los titulos en el documento y los guarda como bloque en un diccionario.
  """
  titles = {}
  for i in range(len(lines) - 1):
    current = lines[i].strip()
    next_line = lines[i+1].strip()
    if is_potential_title_text(current) and is_underline(next_line):
      clean_text = this.clean_line_content(current)
      titles[clean_text] = {
        "char" : next_line[0],
        "length": len(next_line)
      }

  return titles

# El evaluador de continuidad
def group_lines_into_raw_blocks(lines, seek_refs=False):
  """
  Agrupa líneas en bloques lógicos. Cohesiona parrafos fragmentados.
  """
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
    elif is_structural_break(line, False) or (next_line and is_underline(next_line)):
      should_close = True

    if is_underline(line):
      should_close = True

    if should_close and current_acc:
      raw_blocks.append(" ".join(current_acc).strip())
      current_acc = []

  if current_acc:
    raw_blocks.append(" ".join(current_acc).strip())

  return raw_blocks

# El filtro de bloques
def filter_and_format_blocks(raw_blocks, doc_titles, seek_refs=False):
  """
  Limpia, filtra y añade la directiva rST (TOC).
  """

  blocks = []
  blocks.extend(get_toc_directive())

  for rb in raw_blocks:
    # Limpiamos lo que no pudo Pandoc
    clean_text = this.clean_line_content(rb, seek_refs=seek_refs)

    # Despues de limpiar, guardamos si hay contenido
    if not clean_text or this.is_underline(clean_text):
      continue

    if this.is_legacy_toc(clean_text, doc_titles):
      continue

    if clean_text in  doc_titles:
      blocks.append(clean_text)
      continue

    blocks.append(clean_text)

  return blocks
