#!/usr/bin/env python3

import sys, os
import linker

def init_environment():
  """
  Configura el entorno (rutas, logs) sin imports internos
  """
  pass

def main():
    if len(sys.argv) < 2:
        return

    # Detectar si el primer argumento es la bandera de referencias
    seek_refs_mode = "--seek-refs" in sys.argv
    file_args = [arg for arg in sys.argv[1:] if arg != "--seek-refs"]

    for file_path in file_args:
        content = read_file(file_path)
        lines = content.splitlines()
        filename_base = os.path.splitext(os.path.basename(file_path))[0]
        
        if seek_refs_mode:
            from reference_processor import group_refs_blocks

            # No creamos backup (.bak) porque no modificamos la fuente
            ref_blocks = process_rst_blocks(lines, seek_refs=True)
            original_blocks = group_refs_blocks(ref_blocks)

            context_lines = extract_references_context(ref_blocks)

            export_refs_to_out_files(ref_blocks, None, original_blocks)
            print(f"🎯 Referencias extraídas de: {file_path}")
            
        else:
            # --- FLUJO ESTÁNDAR DE REVISIÓN ---
            create_backup(file_path)
            
            # 1. PROTECCIÓN: Identificar y extraer bloques de código
            ranges = identify_literal_blocks(lines)
            protected_lines, blocks_dict = extract_literal_blocks(lines, ranges)
            
            # 2. LIMPIEZA: Metadata y marcas MD obsoletas
            clean_text = strip_metadata("\n".join(protected_lines))
            
            # 3. PROCESAMIENTO: Coordinación de bloques (Mutex automático en False)
            blocks = process_rst_blocks(clean_text.splitlines())
            
            # 4. FORMATEO: Títulos y jerarquía dinámica
            formatted_rst = rst_title_formatter(blocks, filename_base)
            
            # 5. RESTAURACIÓN: Reinyectar el código original
            final_output = reinject_literal_blocks(formatted_rst, blocks_dict)
            
            # Guardado final
            save_file(file_path, final_output)
            print(f"✅ Procesado con éxito (Bloques protegidos: {len(ranges)}): {file_path}")

if __name__ == "__main__":
    main()