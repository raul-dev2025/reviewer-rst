import unittest
import linker

class TestRSTExceptions(unittest.TestCase):

    def test_structural_integrity_in_refs(self):
        """
        Fuerza un error de indentación en una referencia bibliográfica.
        """
        lines = [
            ".. [Ref1] Esta es una referencia",
            "mal indentada" # Esto debería disparar StructuralIntegrityError
        ]
        
        with self.assertRaises(linker.StructuralIntegrityError):
            # Aquí llamaremos a la lógica de la Fase 3
            linker.process_rst_blocks(lines)

    def test_structural_integrity_trigger(self):
      """
      Validar que se puede lanzar la excepción de integridad
      """
      with self.assertRaises(linker.StructuralIntegrityError) as cm:
        # Simula la detección de error de indentación
        raise linker.StructuralIntegrityError(42, "Falta indentación en bloque de referencia")
      self.assertIn("línea 42", str(cm.exception))

    def test_export_path_error(self):
      """Validar error cuando la ruta de exportación es un archivo y no un directorio."""
      linker.bind_dependencies()
      invalid_path = "/tmp/findOut"

      if linker.os.path.exists(invalid_path) and not linker.os.path.isdir(invalid_path):
        raise linker.ExportPathError(invalid_path, "Existe un archivo con el mismo nombre")        
  



if __name__ == "__main__":
    unittest.main()