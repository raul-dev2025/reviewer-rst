# -*- coding: utf-8 -*-
import re
import file_manager, processor, reference_processor, formatter, cleaner, regex


def bind_dependencies():
    """
    Inyecta las dependencias globales en los submódulos 
    para evitar imports locales redundantes.
    """
    # Inyección de la librería estándar
    cleaner.re = re
    processor.re = re
    processor.this = processor
    
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

    # Exposición de símbolos(GateWay)
    read_file = file_manager.read_file
    save_file = file_manager.save_file
    create_backup = file_manager.create_backup
    export_refs_to_out_files = file_manager.export_refs_to_out_files

    # Procesamiento
    process_rst_blocks = processor.process_rst_blocks
    identify_literal_blocks = processor.identify_literal_blocks
    extract_literal_blocks = processor.extract_literal_blocks
    reinject_literal_blocks = processor.reinject_literal_blocks

    # reference_processor
    group_refs_blocks = reference_processor.group_refs_blocks
    extract_references_context = reference_processor.extract_references_context


    # Da formato
    rst_title_formatter = formatter.rst_title_formatter
