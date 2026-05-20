import re

def build_match_and_apply(pattern, search, replace):
    """
    Factoría que genera clausuras (closures) para evaluar y transformar
    dinámicamente cadenas basándose en reglas externas.
    """
    def matches_rules(word):
        return bool(re.search(pattern, word))

    def apply_rule(word):
        return re.sub(search, replace, word)

    return [matches_rules, apply_rule]

def load_dynamic_rules(filepath='archivo_regex.txt'):
    """
    Carga y compila las reglas de transformación del archivo de texto.
    Se prescinde de bloques try-except para permitir que el sistema
    reaccione ante la ausencia o fallo de lectura del archivo de configuración.
    """
    rules = []
    with open(filepath, 'r', encoding='utf-8') as pattern_file:
        for line in pattern_file:
            line = line.strip()
            # Ignorar líneas vacías o comentarios
            if not line or line.startswith('#'):
                continue

            # Desempaquetamos utilizando el delimitador elegido '$'
            parts = [p.strip() for p in line.split('$')]
            if len(parts) == 3:
                pattern, search, replace = parts
                rules.append(build_match_and_apply(pattern, search, replace))

    return rules

def normalize_text_with_rules(text, rules):
    """
    Aplica secuencialmente las reglas dinámicas cargadas sobre el texto.
    """
    modified_text = text
    for matches_rules, apply_rule in rules:
        if matches_rules(modified_text):
            modified_text = apply_rule(modified_text)
    return modified_text