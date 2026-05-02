# -*- coding: utf-8 -*-

import os, shutil
from datetime import datetime

def create_backup(file_path):
    """
    Crea una copia de seguridad del archivo original.
    Si el archivo no existe, levanta una excepción.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    # Creamos un backup con extensión .bak
    # Opcionalmente podrías añadir un timestamp: .20260415.bak
    backup_path = f"{file_path}.bak"
    try:
        shutil.copy2(file_path, backup_path)
        print(f"🚀 Copia de seguridad creada en: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Error crítico al crear backup: {e}")
        raise

def read_file(file_path):
    """Lee el contenido del archivo con codificación UTF-8."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(file_path, content):
    """Guarda el contenido procesado en el archivo original."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def export_refs_to_out_files(all_refs, section_name=None, original_blocks=None):
    """
    Orquesta la generación y escritura de los archivos de salida divididos por formato.
    """
    # Importa las funciones necesarias desde el modulo de referencias
    from reference_processor import extract_references_context, format_references

    output_path = "/tmp/findOut"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    safe_section_name = "".join([c if c.isalnum() else "_" for c in section_name]).strip("_")

    file_name_md = f"out_{safe_section_name}.md"
    file_name_rst = f"out_{safe_section_name}.rst"

    full_path_md = os.path.join(output_path, file_name_md)
    full_path_rst = os.path.join(output_path, file_name_rst)

    # 1. Guarda el contexto
    context_lines = extract_references_context(all_refs)

    # 2. Formato rST para las referencias
    content_rst = format_references(all_refs, rst_format=True)

    # 3. Contexto y referencias en formato markdown
    content_md_lines = "\n".join([f"{item['reference']} - Contexto: {item['context']}" for item in context_lines])
    content_md = "\n".join(content_md_lines)

    # 4. Añade la sección de referencias
    if original_blocks:
      content_md += "\n\n--- Bloque de Referencias Original (Comparativa) ---\n"
      for block in original_blocks:
        content_md += "".join(block)

    # 5. Guardar archivos
    save_file(full_path_md, content_md)
    save_file(full_path_rst, content_rst)

    print(f"📦 Sección exportada a: {full_path_md} y {full_path_rst}")