# -*- coding: utf-8 -*-
# Copyright (c) 2026 Raúl Vílchez Ruiz <r4u1974@gmail.com>
# Distributed under the terms of the MIT License.
# See LICENSE file in the project root for full license information.


def clean_line_content(line, seek_refs=False):
    """Elimina anclajes de Pandoc y repara backticks huérfanos."""
    if not seek_refs:
      # Modo normal, elimina backticks simples
      line = this.re.sub(this.PANDOC_LINK_PATTERN, r'\1\2', line)
    
    # Modo estructural
    # Hay que emparejar las referencias que encontremos, pero tambien borrar o modificar las  antiguas, para que guarden relacion sintactica, con el ancla que deberemos colocar al final del documento(seccion Referencias, agradecimientos y recursos ...)
    else:
      pass

    # 3. Reparar backticks huérfanos (solo si no es un enlace rST válido)
    if line.count('`') % 2 != 0:
        line = line.replace('`', '')
    return line.strip()

def strip_metadata(content):
    """Elimina referencias a cabeceras y metadatos; informacion administrativa."""
    # Eliminar referencias tipo .. _nombre: 
    content = this.re.sub(this.regex.RST_HEADER_PATTERN, '', content)
    # Eliminar directivas contents antiguas 
    content = this.re.sub(this.regex.CONTENTS_DIRECTIVE_PATTERN, '', content, flags=this.re.MULTILINE | this.re.IGNORECASE)
    return content