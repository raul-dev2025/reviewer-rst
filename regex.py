# -*- coding: utf-8 -*-
# Copyright (c) 2026 Raúl Vílchez Ruiz <r4u1974@gmail.com>
# Distributed under the terms of the MIT License.
# See LICENSE file in the project root for full license information.

import re

# Patrones individuales para mayor claridad
REF_BRACKET = r'\[#?[a-zA-Z0-9]+\]'
REF_PANDOC = r'`[^`]+<#?[a-zA-Z0-9]+>`__'
REF_DECLARATION = r'\.\.\s+\[#?[a-zA-Z0-9]+\]'

# Patrones adicionales para limpieza y validación RST
PANDOC_LINK_PATTERN = r'`([^`<>]+(?:``[^`]+``[^`<>]*)*)\s*(<#?[a-zA-Z0-9_-]+>)`__'
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

# --- NUEVOS PATRONES PARA PROCESSOR.PY ---

# Detecta títulos de secciones administrativas (Ignora mayúsculas/minúsculas)
ADMIN_SECTION_PATTERN = re.compile(r'^(?:Referencias|Recursos|Agradecimientos|###)', re.IGNORECASE)

# Detecta el inicio de una nota al pie rST o marcador de referencia: ".. [#]" , "[#f1]" , "[1]"
FOOTNOTE_PATTERN = re.compile(r'^(\.\.\s+)?\[#?[a-zA-Z0-9]+\]')

# Detecta subrayados rST (mínimo 3 caracteres de: = - ~ ^)
RST_UNDERLINE_PATTERN = re.compile(r'^([=\-~^])\1{2,}$')

# Detecta prefijos comunes de listas: guiones, asteriscos o números seguidos de punto o paréntesis (ej: "- ", "1. ", "2) ")
LIST_ITEM_PREFIX_PATTERN = re.compile(r'^\s*(?:[-*]\s+|\d+[.)]\s*)')

# Detecta cualquier estructura de anclaje limpia o con almohadilla para removerla en la comparación (ej: "<#i1>__", "<i2>__")
TOC_ANCHOR_REMOVE_PATTERN = re.compile(r'<#?[a-zA-Z0-9_-]+>')