#!/usr/bin/env python3
import sys
import os

# Gestión de archivos
from file_manager import create_backup, read_file, save_file

# Lógica de transformación
from cleaner import strip_metadata
from formatter import rst_title_formatter
from processor import (
    identify_literal_blocks,
    extract_literal_blocks,
    reinject_literal_blocks,
    process_rst_blocks
    #join_broken_paragraphs
)

def main():
    if len(sys.argv) < 2:
        return

    for file_path in sys.argv[1:]:
        create_backup(file_path)
        content = read_file(file_path)
        lines = content.splitlines()
        filename_base = os.path.splitext(os.path.basename(file_path))[0]
        
        # 1. PROTECCIÓN: Identificar y extraer bloques de código
        ranges = identify_literal_blocks(lines)
        protected_lines, blocks_dict = extract_literal_blocks(lines, ranges)
        
        # 2. LIMPIEZA: Metadata y marcas MD obsoletas sobre el texto protegido
        # Convertimos a string para strip_metadata y luego volvemos a lista
        clean_text = strip_metadata("\n".join(protected_lines))
        
        # 3. PROCESAMIENTO: Unión de párrafos (sin tocar el código oculto)
        blocks = process_rst_blocks(clean_text.splitlines())
        #blocks = join_broken_paragraphs(clean_text.splitlines())
        
        # 4. FORMATEO: Títulos y jerarquía dinámica
        formatted_rst = rst_title_formatter(blocks, filename_base)
        
        # 5. RESTAURACIÓN: Reinyectar el código original en los marcadores
        final_output = reinject_literal_blocks(formatted_rst, blocks_dict)
        
        # Guardado final
        save_file(file_path, final_output)
        print(f"✅ Procesado con éxito (Bloques protegidos: {len(ranges)}): {file_path}")

if __name__ == "__main__":
    main()