# -*- coding: utf-8 -*-
import re
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
is_structural_break = None
get_document_titles = None
filter_and_format_blocks = None
group_lines_into_raw_blocks = None
group_refs_blocks = None
extract_references_context = None
format_references = None
rst_title_formatter = None
get_level_from_symbol = None
render_title = None
clean_line_content = None
strip_metadata = None

def bind_dependencies():
    """
    Inyecta las dependencias globales en los submódulos 
    para evitar imports locales redundantes.
    """
    import exceptions

    # file_manager
    global read_file, save_file, create_backup, export_refs_to_out_files, prepare_file
    # processor
    global is_underline, process_rst_blocks, identify_literal_blocks, extract_literal_blocks, reinject_literal_blocks, is_structural_break, get_document_titles, group_lines_into_raw_blocks, filter_and_format_blocks
    # reference_processor
    global group_refs_blocks, extract_references_context, format_references
    # formatter
    global get_level_from_symbol, render_title, rst_title_formatter
    # cleaner
    global clean_line_content, strip_metadata

    # Inyección de excepiones
    reference_processor.StructuralIntegrityError = exceptions.StructuralIntegrityError

    # Inyección de la librería estándar
    cleaner.re = re
    processor.re = re
    processor.this = processor
    reference_processor.this = processor
    
    # Inyección de constantes de regex en cleaner
    cleaner.PANDOC_LINK_PATTERN = regex.PANDOC_LINK_PATTERN
    cleaner.PANDOC_ANCHOR_PATTERN = regex.PANDOC_ANCHOR_PATTERN
    cleaner.RST_HEADER_PATTERN = regex.RST_HEADER_PATTERN
    cleaner.CONTENTS_DIRECTIVE_PATTERN = regex.CONTENTS_DIRECTIVE_PATTERN
    
    # processor.id_extractor_pattern = regex.id_extractor_pattern

    # Inyección de patrones en processor
    processor.ADMIN_SECTION_PATTERN = regex.ADMIN_SECTION_PATTERN
    processor.FOOTNOTE_PATTERN = regex.FOOTNOTE_PATTERN
    processor.RST_UNDERLINE_PATTERN = regex.RST_UNDERLINE_PATTERN

    # reference_processor module
    reference_processor.reference_pattern = regex.reference_pattern
    reference_processor.rules = closures.load_dynamic_rules('archivo_regex.txt')
    reference_processor.normalize_text_with_rules = closures.normalize_text_with_rules

    # Exposición de símbolos(GateWay)
    read_file = file_manager.read_file
    save_file = file_manager.save_file
    create_backup = file_manager.create_backup
    export_refs_to_out_files = file_manager.export_refs_to_out_files
    reference_processor.prepare_file = file_manager.prepare_file

    # Procesamiento
    is_underline = processor.is_underline
    process_rst_blocks = processor.process_rst_blocks
    identify_literal_blocks = processor.identify_literal_blocks
    extract_literal_blocks = processor.extract_literal_blocks
    reinject_literal_blocks = processor.reinject_literal_blocks
    is_structural_break = processor.is_structural_break
    get_document_titles = processor.get_document_titles
    group_lines_into_raw_blocks = processor.group_lines_into_raw_blocks
    filter_and_format_blocks = processor.filter_and_format_blocks

    # reference_processor
    group_refs_blocks = reference_processor.group_refs_blocks
    extract_references_context = reference_processor.extract_references_context
    format_references = reference_processor.format_references

    # Dar formato, formatter
    rst_title_formatter = formatter.rst_title_formatter

    # cleaner
    strip_metadata = cleaner.strip_metadata
    clean_line_content = cleaner.clean_line_content
