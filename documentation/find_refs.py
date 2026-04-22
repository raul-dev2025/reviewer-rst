import os
import re
import shutil

def extract_reference_blocks(search_term):
    # --- CONFIGURACIÓN ---
    base_dir = "/home/raul-ipa/Repos/web-docs.git/new-docs"
    output_dir = "/tmp/findOut"
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # PATRÓN DE INICIO: Títulos de Referencias/Recursos/Agradecimientos o anclaje [f1]
    ref_start_pattern = re.compile(
        r'(###\s+.*(?:Referencias|Recursos|Agradecimientos).*|\[#?f1\])', 
        re.IGNORECASE
    )
    
    # PATRÓN DE FIN: Cualquier encabezado de nivel 1, 2 o 3 (líneas que empiezan con #)
    # Esto evita que se vuelque el resto del archivo si hay más secciones después.
    section_break_pattern = re.compile(r'^#+\s+', re.MULTILINE)

    found_count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if search_term in file and file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    start_match = ref_start_pattern.search(content)
                    
                    if start_match:
                        found_count += 1
                        output_file = os.path.join(output_dir, f"out{found_count}.md")
                        
                        # Buscamos si hay otra sección después del inicio de las referencias
                        remainder = content[start_match.start():]
                        # Buscamos el siguiente título saltando el que acabamos de encontrar
                        # Buscamos a partir de la segunda línea del bloque extraído
                        lines = remainder.splitlines()
                        block_lines = [lines[0]] # Empezamos con la línea del título/anclaje
                        
                        for line in lines[1:]:
                            # Si encontramos otro encabezado, paramos de añadir líneas
                            if section_break_pattern.match(line):
                                break
                            block_lines.append(line)
                        
                        clean_block = "\n".join(block_lines).strip()
                        
                        with open(output_file, 'w', encoding='utf-8') as out:
                            out.write(f"--- SOURCE: {file_path} ---\n")
                            out.write("-" * 60 + "\n\n")
                            out.write(clean_block)
                        
                        print(f"✅ [{found_count}] Bloque recortado de: {file}")
                
                except Exception as e:
                    print(f"🛑 Error en {file_path}: {e}")

    print(f"\n✨ Listo. Revisa los bloques específicos en {output_dir}")

if __name__ == "__main__":
    extract_reference_blocks("initrd")