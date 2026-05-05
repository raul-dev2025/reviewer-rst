# -*- coding: utf-8 -*-
import re

# Patrones individuales para mayor claridad
REF_BRACKET = r'\[#?[a-zA-Z0-9]+\]'
REF_PANDOC = r'`[^`]+<#?[a-zA-Z0-9]+>`__'
REF_DECLARATION = r'\.\.\s+\[#?[a-zA-Z0-9]+\]'

# Patrones adicionales para limpieza y validación RST
PANDOC_LINK_PATTERN = r'`([^<]+)\s*<[^>]+>`__'
PANDOC_ANCHOR_PATTERN = r'\s*<#?[a-zA-Z0-9]+>`__'
RST_HEADER_PATTERN = r'\.\. _[a-zA-Z0-9_-]+:\n*'
CONTENTS_DIRECTIVE_PATTERN = r'^\.\. contents::.*?\n(\s+:[a-z]+:.*?\n)*'

# Expresión regular combinada usando alternancia
# Utiliza grupos de no captura para evaluar cualquiera de los tres formatos
reference_pattern = re.compile(
    rf'(?:{REF_BRACKET}|{REF_PANDOC}|{REF_DECLARATION})'
)

# Patrón estricto para extraer únicamente el identificador (ej. f1, f2, 1) sin corchetes
id_extractor_pattern = re.compile(r'#?([a-zA-Z0-9]+)')