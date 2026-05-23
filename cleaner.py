# -*- coding: utf-8 -*-

def clean_line_content(line):
    """Elimina anclajes de Pandoc y repara backticks huérfanos."""
    # 1. Elimina el formato de enlace rST dejando solo el texto: `Texto <#ref>`__ -> Texto
    line = this.re.sub(this.PANDOC_LINK_PATTERN, r'\1', line)

    # 2. Eliminar anclajes sueltos <#i1i2>`__ 
    line = this.re.sub(this.PANDOC_ANCHOR_PATTERN, '', line)
    
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