# -*- coding: utf-8 -*-

import unittest
import linker, cleaner

class TestRSTRefactor(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    """
    Configura el entorno (rutas, logs) sin imports internos
    """
    linker.bind_dependencies()

  def test_is_underline(self):
      """
      Validar la deteccion de subrayados rST.
      Regla: minimo 3 caracteres, todos identicos del set [=, -, ~, ^]
      """

      # Deben ser ciertos
      self.assertTrue(linker.is_underline("======"))
      self.assertTrue(linker.is_underline("------"))
      self.assertTrue(linker.is_underline("^^^"))
      
      #Deben ser falsos
      self.assertFalse(linker.is_underline("Frase de ejemplo"))
      self.assertFalse(linker.is_underline("=="))
      self.assertFalse(linker.is_underline("==-=="))
      self.assertFalse(linker.is_underline(""))

  def test_is_structural_break(self):
      """
      Validacion de puntos de ruptura estructural
      """

      self.assertTrue(linker.is_structural_break(""), "Una línea vacía debe romper el bloque")
      self.assertTrue(linker.is_structural_break(".. nota:"), "Las  directivas rST son rupturas")
      self.assertTrue(linker.is_structural_break("::"), "El inicio de bloque es ruptura")
      self.assertTrue(linker.is_structural_break(":autor:"), "Si empieza por dos puntos es ruptura")
      self.assertTrue(linker.is_structural_break("   :autor:"), "Los  campos indentados son ruptura")

      self.assertFalse(linker.is_structural_break("esto es texto normal"), "texto normal no rompe")
      self.assertFalse(linker.is_structural_break("  continuación texto"), "indentación no rompe")

      self.assertTrue(linker.is_structural_break("Referencias", seek_refs=True))
      self.assertTrue(linker.is_structural_break("[1] Referencia técnica", seek_refs=True))
      self.assertTrue(linker.is_structural_break(".. [#] Nota al pie", seek_refs=True))
      
  def test_rst_title_formatter(self):
      """
      Validez del formato aplicado al texto
      - ajuste de longitud y referencia atomica
      """

      from formatter import rst_title_formatter
      
      blocks = ["Titulo de prueba", "===================="]
      filename = "guia_usuario"
      
      result = rst_title_formatter(blocks, filename)
      
      self.assertIn(".. _guia_usuario_1:", result)
      
      expected_underline = "=" * len("Titulo de prueba")
      self.assertIn(expected_underline, result)
      
      self.assertIn(expected_underline, result)

  def test_integration_messy_paragraph(self):
      """
      Validacionde integracion: paragrafos con indentacion
      y mantenimiento de la estructura
      """
      from processor import process_rst_blocks
      from  formatter import rst_title_formatter
      input_data = [
          "Consiste en un ``device_node``\\ s -nodo de dispositivo, en forma de",
          "     *estructura de árbol*,",
          "descrita más abajo.",
          "",
          "Siguiente Párrafo."
      ]

      blocks = process_rst_blocks(input_data)

      # Ahora esperamos 3 bloques de TOC + 2 de contenido = 5
      self.assertEqual(len(blocks), 4)

      # Los párrafos reales empiezan tras el TOC (índice 3 en adelante)
      self.assertIn("forma de *estructura de árbol*, descrita", blocks[2])
      
      result = rst_title_formatter(blocks, "test_file")
      self.assertNotIn("====", result)
      self.assertIn("Consiste en un", result)

  def test_level_1_title_decoration(self):
      """
      Validar nivel de titulo 1 con sobre-subrayado,
      y esta redeado por lineas en vacias.
      """
      from formatter import rst_title_formatter

      blocks = ["TITULO PRINCIPAL", "================="]
      filename = "doc_test"
      
      result = rst_title_formatter(blocks, filename)
      
      expected_pattern = (
          ".. _doc_test_1:\n\n"
          "================\n"
          "TITULO PRINCIPAL\n"
          "================\n"
      )
      
      self.assertIn(expected_pattern, result)

  def test_clean_line_content(self):
      """
      Validar marcas md obsoletas y restos de Pandoc no revisados!
      """

      input_1 = "Capa de memoria <#i2>`__"
      input_2 = "Capa de memoria <i2>`__"
      self.assertEqual(cleaner.clean_line_content(input_1), "Capa de memoria")
      self.assertEqual(cleaner.clean_line_content(input_2), "Capa de memoria")

  def test_identify_literal_blocks(self):
      """
      Valida la identificacion de bloques de codigo.
      """
      from processor import identify_literal_blocks
      lines = [
          "Párrafo inicial.",          # 0
          "",                          # 1
          "::",                        # 2 (Inicio bloque 1)
          "   Contenido indentado",    # 3
          "   más contenido",          # 4
          "",                          # 5 (Línea vacía interna)
          "   fin del bloque",         # 6 (Fin bloque 1)
          "Párrafo de salida.",        # 7 (Rompe indentación)
          ".. code-block:: bash",      # 8 (Inicio bloque 2)
          "",                          # 9
          "   echo 'hola'",            # 10 (Fin bloque 2)
          "Final."                     # 11
      ]
      lines2 = [
          "Párrafo inicial.",          # 0
          "",                          # 1
          "::",                        # 2 (Inicio bloque 1)
          "   Contenido indentado",    # 3
          "   más contenido",          # 4
          "",                          # 5 (Línea vacía interna)
          "   más contenido",          # 6
          "   fin del bloque",         # 7 (Fin bloque 1)
          "",                          # 8 (Línea vacía)
          "Párrafo de salida.",        # 9 (Rompe indentación)
          "",                          # 10 (Línea vacía)
          ".. code-block:: bash",      # 11 (Inicio bloque 2)
          "",                          # 12
          "   echo 'hola'",            # 13 (Fin bloque 2)
          "",                          # 14
          "Final."                     # 15
      ]
      lines3 = [
          "Párrafo inicial.",          # 0
          "",                          # 1
          "::",                        # 2 (Inicio bloque 1)
          "",                          # 3 (Línea vacía)
          "   Contenido indentado",    # 4
          "   más contenido",          # 5
          "",                          # 6 (Línea vacía interna)
          "   más contenido",          # 7
          "   fin del bloque",         # 8 (Fin bloque 1)
          "",                          # 9 (Línea vacía)
          "Párrafo de salida.",        # 10 (Rompe indentación)
          "Párrafo de salida.",        # 11 (Rompe indentación)
          "",                          # 12 (Línea vacía)
          ".. code-block:: bash",      # 13 (Inicio bloque 2)
          "",                          # 14
          "   echo 'hola'",            # 15 (Fin bloque 2)
          "",                          # 16
          "Final."                     # 17
      ]
      ranges = identify_literal_blocks(lines)
      self.assertEqual(ranges, [(2, 6), (8, 10)])
      ranges = identify_literal_blocks(lines2)
      self.assertEqual(ranges, [(2, 7), (11, 13)])
      ranges = identify_literal_blocks(lines3)
      self.assertEqual(ranges, [(2, 8), (13, 15)])

  def test_extract_literal_blocks(self):
    """
    Verifica que el codige es extraido adecuadamente y
    sustituido por un marcador.
    """
    from processor import identify_literal_blocks, extract_literal_blocks
    lines = [
       "Texto inicial",     # 1
       "::",                # 2
       "   codigo 1",       # 3
       "Texto medio",       # 4
       ".. code-block::",   # 5
       "   codigo 2"        # 6
    ]
    ranges = identify_literal_blocks(lines)
    new_lines, blocks_dict = extract_literal_blocks(lines, ranges)
    # Comprueba cuantas lineas quedan
    self.assertEqual(len(new_lines), 4)
    # Comprueba posicion del marcador
    self.assertEqual(new_lines[1], "[[CODE_BLOCK_0]]")
    self.assertEqual(new_lines[3], "[[CODE_BLOCK_1]]")
    # El texto recuperado debe ser el correcto
    self.assertIn("   codigo 1", blocks_dict["[[CODE_BLOCK_0]]"])
    self.assertIn("   codigo 2", blocks_dict["[[CODE_BLOCK_1]]"])

  def test_full_block_cycle(self):
    """
    Valida el ciclo completo: extraccion, proceso intermedio, reinsercion
    """
    from processor import identify_literal_blocks, extract_literal_blocks, reinject_literal_blocks
    lines = [
       "titulo minusculo",
       "::",
       "   codigo intacto 100%",
       "parrafo final"
    ]
    # 1 Identifica y extrae
    ranges = identify_literal_blocks(lines)
    lines_with_markers, blocks_dict = extract_literal_blocks(lines, ranges)
    # 2. Simula el proceso de formato, comprobando que lo guardado
    # en el diccionario continua intacto
    formatted_lines = [l.upper() for l in lines_with_markers]
    text_ready = "\n".join(formatted_lines)
    # 3.
    final_output = reinject_literal_blocks(text_ready, blocks_dict)
    # Verificacion
    self.assertIn("TITULO MINUSCULO", final_output)
    self.assertIn("PARRAFO FINAL", final_output)
    # El codigo debera estar intacto
    self.assertIn("   codigo intacto 100%", final_output)

  def test_dynamic_hierarchy_logic(self):
    """
    Valida el simbolo utilizado para definir jerarquia de
    niveles en los titulos del cocumento.
    Solo puede haber un titulo de documento: ====
    """
    from formatter import rst_title_formatter

    lines_1 = [
        "Titulo A", "---------", # Detectado como Nivel 0 (Caja ===)
        "Texto",
        "Titulo B", "^^^^^^^^^", # Detectado como Nivel 1 (Subrayado ===)
        "Texto",
        "Titulo C", "=========", # Detectado como Nivel 2 (Subrayado ---)
        "Texto",
        "Titulo D", "=========", # Repite símbolo -> Sigue siendo Nivel 2
        "Texto",
        "Titulo E", "~~~~~~~~~"  # Detectado como Nivel 3 (Subrayado ^^^)
    ]

    # ESCENARIO 2: Proteccion del Nivel 1
    # El autor usa '===' para el Nivel 1, y luego repite '===' mas tarde.
    lines_2 = [
        "Principal", "=========", # Nivel 0
        "Texto",
        "Subtitulo", "---------", # Nivel 1
        "Sub-Sub",   "^^^^^^^^^", # Nivel 2
        "Otro N1?",  "=========", # REPETICIÓN: Nivel disponible no repetido/aparecido
        "Mini",      "~~~~~~~~~"  # Nivel 4
    ]

    # Caso: El autor usa '---' como primer título (debe ser Nivel 1 -> Caja =)
    # Luego usa '===' (debe ser Nivel 2 -> Subrayado -)
    # Luego repite '---' (debe ser Nivel 2 porque el 1 es intocable)
    lines_3 = [
        "Titulo Uno", "-------", 
        "Texto",
        "Titulo Dos", "=======",
        "Texto",
        "Titulo Tres", "-------"
    ]

    # empaqueta la llamada a la funcion
    res_1 = rst_title_formatter(lines_1, "test1")
    res_2 = rst_title_formatter(lines_2, "test2")
    res_3 = rst_title_formatter(lines_3, "doc")

    # Verificacion escenario 1
    # El primer titulo es una caja sobre-subrayado
    self.assertIn("========\nTitulo A\n========", res_1)
    # 
    self.assertIn("Titulo C\n--------", res_1)

    # Verificacion escenario 3    
    self.assertIn("Otro N1?\n~~~~~~~~", res_2)

    # 1. Rodeado por el simbolo de primer Nivel "="
    self.assertIn("==========\nTitulo Uno\n==========", res_3)
    # 2. Subrayado de nivel dos "-"    
    self.assertIn("Titulo Dos\n==========", res_3)
    # 3. Subrayado de nivel dos "-" por que repite simbolo
    self.assertIn("Titulo Tres\n----------", res_3)

  def test_join_paragraph_with_lowercasee_continuation(self):
    """
    Valida parrafo si encuentra lineas separadas sin signos de puntuacion;
    al principio o al final.
    """
    from processor import process_rst_blocks

    lines = [
      "causada por",
      "",
      "efectiva desaparicion"
    ]

    blocks = process_rst_blocks(lines)
    self.assertEqual(blocks[2], "causada por efectiva desaparicion")

  # Primer test propuesto: get_documet_titles()
  # El recolector
  def test_get_documet_titles(self):
    """
    Valida la identificacion de textos, despues del subrrayado.
    """
    from processor import get_document_titles

    lines = [
      "Titulo Uno",
      "==========",
      "Este es un parrafo intermedio",
      "",
      "`Introduccion <#i1>`__",
      "---------------------",
      "Otro parrafo",
      "Titulo Final",
      "~~~~~~~~~~~~"      
    ]

    titles = get_document_titles(lines)

    # Se espera tres titulos y contaremos 
    # a partir de la cuarta entrada en bloque
    self.assertEqual(len(titles), 3)
    self.assertEqual(titles[0], "Titulo Uno")
    self.assertEqual(titles[1], "`Introduccion <#i1>`__")
    self.assertEqual(titles[2], "Titulo Final")

  # Segundo test propuesto: group_lines_into_raw_blocks()
  # El evaluador de continuidad
  def test_group_lines_into_raw_blocks(self):
    """
    Verifica si la funcion une el texto que empieza
    por minuscula despues de linea vacia
    """
    from processor import group_lines_into_raw_blocks

    lines = [
      "Esta frase esta",
      "",
      "continuada en minuscula."
    ]

    blocks = group_lines_into_raw_blocks(lines)

    self.assertEqual(len(blocks), 1)
    self.assertEqual(blocks[0], "Esta frase esta continuada en minuscula.")

  # Tercer test propuesto: filter_and_format_blocks()
  # El filtro de bloques
  def test_filter_and_format_blocks(self):
    """
    Valida que el filtro de bloques, limpie los anclajes .md,
    elimine el indice viejo y adhiera la ditectiva de contenido.
    """
    from processor import filter_and_format_blocks

    # Simulamos lo que retorna la parte 2; el texto pristino
    doc_titles = ["Introduccion", "Capa de memoria"]
    raw_blocks = [      
      "`Introduccion <#i1>`__ `Capa de memoria <#i2>`__",
      "`Introduccion <#i1>`__",
      "Este es un párrafo con un enlace `interno <#ref>`__"
    ]

    final_blocks = filter_and_format_blocks(raw_blocks, doc_titles)

    # Lo que debe devolver:
    # 1. la directiva de contenido
    expected_toc = ".. contents:: Tabla de contenidos\n   :depth: 3"
    self.assertEqual(final_blocks[0], expected_toc)
    
    # 2. El indice arrastrado desde markdowns y los anclajes
    # ya han sido procesados (raw_blocks[0-1])
    self.assertEqual(final_blocks[2], "Introduccion")

    # 3. El parrafo (raw_blocks[2]) debe estar limpio
    self.assertEqual(final_blocks[3], "Este es un párrafo con un enlace interno")

    # 4. total esperad: 3 (TOC) + 2 (contenido limpio) = 5
    self.assertEqual(len(final_blocks), 4)

  def test_full_reference_processing(self):
    """
    Comprueba que una nota de pie de página y su enlace son procesados e identificados
    correctamente como un bloque de referencias usando la convención rST estándar.
    """
    from processor import process_rst_blocks
    
    lines = [
        "En el hipervisor deben ser deshabilitadas las trampas (traps) [#f1]_.",
        "",
        ".. [#f1] Traps, conjunto especial de instrucciones.",
        "   Ver `CPUID wikipedia <https://en.wikipedia.org/wiki/CPUID>`__"
    ]
    
    # Procesamos en modo referencias
    blocks = process_rst_blocks(lines, seek_refs=True)
    
    # Verificamos que se haya capturado el bloque de referencia
    self.assertTrue(len(blocks) > 0, "Debería haberse detectado el bloque de referencia.")
    self.assertIn("[#f1]", blocks[0], "El bloque debe contener el identificador de la nota.")

  def test_group_refs_blocks(self):
    """
    Verifica el formato correcto de referencias en un documento.
    """
    import os
    from reference_processor import group_refs_blocks
    from file_manager import save_file

    # 1. Simula una seccion de referencias
    sample_lines = [
      "Referencias",
      "-----------",
      "",
      "[#f1] Almesberger, Werner; \"Booting Linux: The History and the Future\"",
      "    http://www.almesberger.net/cv/papers/ols2k-9.ps.gz",
      "[#f2] newlib package (experimental), with initrd example",
      "    https://www.sourceware.org/newlib/",
      "[#f3] util-linux: Miscellaneous utilities for Linux",
      "    https://www.kernel.org/pub/linux/utils/util-linux/",
      "   [f5] situando en memoria, o trampa de arranque -bootstrapping."
    ]

    # 2. Probar group_refs_blocks, maquina de estado
    print("--- Probando group_refs_blocks() ---")
    blocks = group_refs_blocks(sample_lines)

    for idx, b in enumerate(blocks):
      print(f"Bloque {idx + 1}: {len(b)} lineas")

    

  # def test_format_references(self):
  #   """
  #   Simula referencias encontradas en el documento, y verifica el formato.
  #   """
  #   from reference_processor import format_references
  #   # 3. Simular referencias encontradas
  #   sample_refs = ["#f1", "[#f2]", "`f3 <#f3>`_", "f5"]

  #   # 4. Probar format_references()
  #   print("\n--- Probando format_references() a rST ---")
  #   formatted_rst = format_references(sample_refs, rst_format=True)
  #   print(formatted_rst)

  # def test_extract_references_context(self):
  #   """
  #   Valida la extraccion del contexto asociado a la referencia.
  #   """
  #   from reference_processor import extract_references_context, format_references

  #   # Usamos texto de documento real donde la referencia aparece en el cuerpo
  #   document_lines = [
  #     "Esta es una frase de prueba que usa [#f1] como ejemplo.",
  #     "Aquí hay otro texto de contexto para f5.",
  #     "contexto de texto 2 [#f2]",
  #     "otro contexto `f3 <#f3>`_"
  #   ]

  #   # 5. Probar extract_references_context()
  #   print("\n--- Probando extract_references_context() ---")
  #   contexts = extract_references_context(document_lines)

  #   for c in contexts:
  #     print(f"ref : {c['reference']}, context: {c['context']}")
    
  #   self.assertTrue(len(contexts) > 0, "Debería haberse extraído contexto del documento.")



if __name__ == "__main__":
    unittest.main()
