#!/usr/bin/env python3

import sys, os
import linker

def init_environment():
  """
  Configura el entorno (rutas, logs) sin imports internos
  """
  linker.bind_dependencies()

def main():
    if len(sys.argv) < 2:
        return

    init_environment()

    # Detectar si el primer argumento es la bandera de referencias
    seek_refs_mode = "--seek-refs" in sys.argv
    file_args = [arg for arg in sys.argv[1:] if arg != "--seek-refs"]

    for file_path in file_args:
        content = linker.file_manager.read_file(file_path)
        lines = content.splitlines()
        filename_base = os.path.splitext(os.path.basename(file_path))[0]
        
        if seek_refs_mode:
            # No creamos backup (.bak) porque no modificamos la fuente
            ref_blocks = linker.process_rst_blocks(lines, seek_refs=True)
            original_blocks = linker.group_refs_blocks(ref_blocks)
            context_lines = linker.extract_references_context(ref_blocks)

            linker.export_refs_to_out_files(ref_blocks, None, original_blocks)
            print(f"🎯 Referencias extraídas de: {file_path}")
            
        else:
            # --- FLUJO ESTÁNDAR DE REVISIÓN ---
            linker.create_backup(file_path)
            
            # 1. PROTECCIÓN: Identificar y extraer bloques de código
            ranges = linker.identify_literal_blocks(lines)
            protected_lines, blocks_dict = linker.extract_literal_blocks(lines, ranges)
            
            # 2. LIMPIEZA: Metadata y marcas MD obsoletas
            clean_text = linker.strip_metadata("\n".join(protected_lines))
            
            # 3. PROCESAMIENTO: Coordinación de bloques (Mutex automático en False)
            blocks = linker.process_rst_blocks(clean_text.splitlines())
            
            # 4. FORMATEO: Títulos y jerarquía dinámica
            formatted_rst = linker.rst_title_formatter(blocks, filename_base)
            
            # 5. RESTAURACIÓN: Reinyectar el código original
            final_output = linker.reinject_literal_blocks(formatted_rst, blocks_dict)
            
            # Guardado final
            linker.save_file(file_path, final_output)
            print(f"✅ Procesado con éxito (Bloques protegidos: {len(ranges)}): {file_path}")

if __name__ == "__main__":
    main()