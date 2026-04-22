def is_structural_break(line, seek_refs=False):
  stripped = line.strip()
  if not stripped:
    return False

  if seek_refs:
    # Mutex referencias, desactiva bloques
    ref_start_pattern = re.compile(
      r'(###\s+.*(?:Referencias|Recursos|Agradecimientos).*|\[#?f1\])',
      re.IGNORECASE
    )
    return bool(ref_start_pattern.search(stripped))

  else:
    # Mutex bloques, desactiva referencias    
    return stripped.startswith('.. ') or stripped.startswith('   :') or stripped.startswith('::')