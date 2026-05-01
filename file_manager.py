# -*- coding: utf-8 -*-

import os
import shutil
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

def export_refs_to_out_files(all_refs, section_name=None):
    """
    Orquesta la generación y escritura de los archivos de salida divididos por formato.
    """
    output_path = "/tmp/findOut"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    safe_section_name = "".join([c if c.isalnum() else "_" for c in section_name]).strip("_")

    file_name_md = f"out_{safe_section_name}.md"
    file_name_rst = f"out_{safe_section_name}_rST.md"

  output_path = "/tmp/findOut"

  if not os.path.exists(output_path):
    os.makedirs(output_path)

  for i, block in enumerate(all_blocks, start=1):
    file_name = f"out{i}.md"
    full_path = os.path.join(output_path, file_name)

    with open(full_path, 'w', encoding='utf-8') as f:
      f.writelines(block)

    print(f"📦 Bloque de referencias exportado a: {full_path}")

    