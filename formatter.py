# -*- coding: utf-8 -*-

this = None

LEVEL_STYLES = {
    0: {'char': "=", 'overline': True},  # Título del documento (Caja)
    1: {'char': "=", 'overline': False}, # Sección
    2: {'char': "-", 'overline': False}, # Subsección
    3: {'char': "~", 'overline': False}, # ...
    4: {'char': "^", 'overline': False},
}

# El planificador
def get_level_from_symbol(symbol, state):
  """
  Resuelve el nivel de titulo en base al primer simbolo definido en el documento.
  """
  # Si el simbolo aparece por primera vez.
  if symbol not in state["mapping"]:
    current_level = state["next_available_level"]
    state["mapping"][symbol] = current_level

    if state["next_available_level"] < 4:
      state["next_available_level"] +=1
    return current_level

  # Si ya es conocido
  assigned_level = state["mapping"][symbol]

  # REGLA DE PROTECCIÓN: Si reaparece el símbolo del Título del Documento (0),
  # en adelante sera nivel 1
  if assigned_level == 0 and state["title_counter"] > 0:
    return state["next_available_level"]

  return assigned_level

# La imprenta
def render_title(text, level, filename_base, state):
  """
  Immprime el titulo rST, con anclajes y estilo apropiados.
  """
  state["title_counter"] +=1
  output = []

  # Anclajes
  output.append(f".. _{filename_base}_{state['title_counter']}:")
  output.append("")

  # Recuperamos el estilo de nuestra metodología (default a Nivel 1 si falla)
  style = LEVEL_STYLES.get(level, LEVEL_STYLES[1])

  # El caracter utilizado para el titulo
  char = style['char']
  underline = char * len(text)

  if style.get('overline', False):
    output.append(underline)
    output.append(text)
    output.append(underline)
  else:
    output.append(text)
    output.append(underline)

  output.append("")
  return "\n".join(output)

# El organizador
def rst_title_formatter(blocks, filename_base):
  state = {
    "mapping": {},           # Ej: {'=': 0, '-': 1}
    "next_available_level": 0, # Empezamos en 0 (Título Principal)
    "level_0_symbol": None,    # El símbolo sagrado del documento
    "title_counter": 0         # Para generar anclajes únicos
  }

  final_output = []
  i = 0 
  while i < len(blocks):
    current = blocks[i].strip()
    next_b = blocks[i+1].strip() if i+1 < len(blocks) else ""

    if this.is_potential_title_text(current) and this.is_underline(next_b):
      symbol = next_b[0]

      # Establece el nivel
      level = get_level_from_symbol(symbol, state)

      # Imprime
      rendered = render_title(current, level, filename_base, state)
      final_output.append(rendered)

      # Salta texto y subrayado
      i += 2

    else:
      if current:
        final_output.append(current)
        final_output.append("")

      i += 1

  return "\n".join(final_output)


