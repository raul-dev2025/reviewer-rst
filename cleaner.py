# -*- coding: utf-8 -*-
import re
import cleaner

def clean_line_content(line):
    """Elimina anclajes de Pandoc y repara backticks huérfanos."""
    # 1. Elimina el formato de enlace rST dejando solo el texto: `Texto <#ref>`__ -> Texto
    line = re.sub(cleaner.PANDOC_LINK_PATTERN, r'\1', line)

    # 2. Eliminar anclajes sueltos <#i1i2>`__ 
    line = re.sub(cleaner.PANDOC_ANCHOR_PATTERN, '', line)
    
    # 3. Reparar backticks huérfanos (solo si no es un enlace rST válido)
    if line.count('`') % 2 != 0:
        line = line.replace('`', '')
    return line.strip()

def strip_metadata(content):
    """Elimina referencias a cabeceras y metadatos; informacion administrativa."""
    # Eliminar referencias tipo .. _nombre: 
    content = re.sub(cleaner.RST_HEADER_PATTERN, '', content)
    # Eliminar directivas contents antiguas 
    content = re.sub(cleaner.CONTENTS_DIRECTIVE_PATTERN, '', content, flags=re.MULTILINE | re.IGNORECASE)
    return content