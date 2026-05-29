# -*- coding: utf-8 -*-
# Copyright (c) 2026 Raúl Vílchez Ruiz <r4u1974@gmail.com>
# Distributed under the terms of the MIT License.
# See LICENSE file in the project root for full license information.

import re, os, sys, shutil
import file_manager, processor, reference_processor, formatter, cleaner, regex, closures

# Definimos los símbolos a nivel de módulo para que existan en el namespace
read_file = None
save_file = None
create_backup = None
export_refs_to_out_files = None
prepare_file = None
is_underline = None
process_rst_blocks = None
identify_literal_blocks = None
extract_literal_blocks = None
reinject_literal_blocks = None
is_legacy_toc = None
is_structural_break = None
get_document_titles = None
filter_and_format_blocks = None
group_lines_into_raw_blocks = None
group_refs_blocks = None
extract_references_context = None
format_references = None
rst_title_formatter = None
is_potential_title_text = None
StructuralIntegrityError = None
ExportPathError = None
clean_line_content = None
PANDOC_LINK_PATTERN = None
PANDOC_ANCHOR_PATTERN = None
FOOTNOTE_PATTERN = None
reference_pattern = None
ADMIN_SECTION_PATTERN = None
RST_UNDERLINE_PATTERN = None
get_level_from_symbol = None
render_title = None
clean_line_content = None
strip_metadata = None
TOC_ANCHOR_REMOVE_PATTERN = None
LIST_ITEM_PREFIX_PATTERN = None


def bind_dependencies():
    """
    Inyecta las dependencias globales en los submódulos 
    para evitar imports locales redundantes.
    """
    import exceptions

    # Exceptions
    global StructuralIntegrityError, ExportPathError, RSTProcessorError
    # file_manager
    global read_file, save_file, create_backup, export_refs_to_out_files, prepare_file
    # processor
    global is_underline, process_rst_blocks, identify_literal_blocks, extract_literal_blocks, reinject_literal_blocks, is_structural_break, get_document_titles, is_legacy_toc, group_lines_into_raw_blocks, filter_and_format_blocks, is_potential_title_text
    # reference_processor
    global group_refs_blocks, extract_references_context, format_references
    # formatter
    global get_level_from_symbol, render_title, rst_title_formatter
    # cleaner
    global clean_line_content, strip_metadata
    # regex
    global reference_pattern, ADMIN_SECTION_PATTERN, RST_UNDERLINE_PATTERN, PANDOC_LINK_PATTERN, PANDOC_ANCHOR_PATTERN, FOOTNOTE_PATTERN, LIST_ITEM_PREFIX_PATTERN, TOC_ANCHOR_REMOVE_PATTERN


    # Inyección de excepiones
    reference_processor.StructuralIntegrityError = exceptions.StructuralIntegrityError
    processor.StructuralIntegrityError = exceptions.StructuralIntegrityError
    StructuralIntegrityError = exceptions.StructuralIntegrityError
    ExportPathError = exceptions.ExportPathError
    
    # Inyección de constantes de regex en cleaner
    PANDOC_LINK_PATTERN = regex.PANDOC_LINK_PATTERN
    PANDOC_ANCHOR_PATTERN = regex.PANDOC_ANCHOR_PATTERN
    FOOTNOTE_PATTERN = regex.FOOTNOTE_PATTERN
    RST_HEADER_PATTERN = regex.RST_HEADER_PATTERN
    CONTENTS_DIRECTIVE_PATTERN = regex.CONTENTS_DIRECTIVE_PATTERN
    
    # Inyección de patrones en processor
    processor.ADMIN_SECTION_PATTERN = regex.ADMIN_SECTION_PATTERN
    processor.FOOTNOTE_PATTERN = regex.FOOTNOTE_PATTERN
    processor.RST_UNDERLINE_PATTERN = regex.RST_UNDERLINE_PATTERN
    processor.LIST_ITEM_PREFIX_PATTERN = regex.LIST_ITEM_PREFIX_PATTERN
    processor.TOC_ANCHOR_REMOVE_PATTERN= regex.TOC_ANCHOR_REMOVE_PATTERN

    # reference_processor module
    reference_processor.reference_pattern = regex.reference_pattern
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_regex = os.path.join(base_dir, 'archivo_regex.txt')
    reference_processor.rules = closures.load_dynamic_rules(ruta_regex)
    reference_processor.normalize_text_with_rules = closures.normalize_text_with_rules
    reference_processor.StructuralIntegrityError = exceptions.StructuralIntegrityError

    # Exposición de símbolos(GateWay)
    read_file = file_manager.read_file
    save_file = file_manager.save_file
    create_backup = file_manager.create_backup
    export_refs_to_out_files = file_manager.export_refs_to_out_files
    prepare_file = file_manager.prepare_file
    reference_processor.prepare_file = file_manager.prepare_file

    # Procesamiento
    is_underline = processor.is_underline
    process_rst_blocks = processor.process_rst_blocks
    identify_literal_blocks = processor.identify_literal_blocks
    extract_literal_blocks = processor.extract_literal_blocks
    reinject_literal_blocks = processor.reinject_literal_blocks
    is_legacy_toc = processor.is_legacy_toc
    is_structural_break = processor.is_structural_break
    get_document_titles = processor.get_document_titles
    group_lines_into_raw_blocks = processor.group_lines_into_raw_blocks
    filter_and_format_blocks = processor.filter_and_format_blocks
    is_potential_title_text = processor.is_potential_title_text

    # reference_processor
    group_refs_blocks = reference_processor.group_refs_blocks
    extract_references_context = reference_processor.extract_references_context
    format_references = reference_processor.format_references

    # Dar formato, formatter
    rst_title_formatter = formatter.rst_title_formatter

    # cleaner
    strip_metadata = cleaner.strip_metadata
    clean_line_content = cleaner.clean_line_content

    # regex
    reference_pattern = regex.reference_pattern
    ADMIN_SECTION_PATTERN = regex.ADMIN_SECTION_PATTERN
    RST_UNDERLINE_PATTERN = regex.RST_UNDERLINE_PATTERN
    PANDOC_LINK_PATTERN = regex.PANDOC_LINK_PATTERN
    PANDOC_ANCHOR_PATTERN = regex.PANDOC_ANCHOR_PATTERN
    FOOTNOTE_PATTERN = regex.FOOTNOTE_PATTERN
    TOC_ANCHOR_REMOVE_PATTERN = regex.TOC_ANCHOR_REMOVE_PATTERN
    LIST_ITEM_PREFIX_PATTERN = regex.LIST_ITEM_PREFIX_PATTERN

    # Inyección de la librería estándar
    current_module = sys.modules[__name__]
    cleaner.regex = regex
    cleaner.this = current_module
    processor.re = re
    processor.StructuralIntegrityError = exceptions.StructuralIntegrityError
    processor.this = current_module
    file_manager.this = current_module
    reference_processor.this = current_module
    closures.re = re
    closures.this = current_module
    formatter.this = current_module
    file_manager.os = os
    file_manager.shutil = shutil
    file_manager.FileNotFoundError = FileNotFoundError
    file_manager.ExportPathError = exceptions.ExportPathError
    file_manager.this = current_module
    processor.read_file = file_manager.read_file