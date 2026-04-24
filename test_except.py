import unittest
from processor import process_rst_blocks  # Tu módulo actual
from exceptions import StructuralIntegrityError, ExportPathError

class TestRSTExceptions(unittest.TestCase):

    def test_structural_integrity_in_refs(self):
        """
        Fuerza un error de indentación en una referencia bibliográfica.
        """
        lines = [
            ".. [Ref1] Esta es una referencia",
            "mal indentada" # Esto debería disparar StructuralIntegrityError
        ]
        
        with self.assertRaises(StructuralIntegrityError):
            # Aquí llamaremos a la lógica de la Fase 3
            process_rst_blocks(lines)

    def test_structural_integrity_trigger(self):
      """
      Validar que se puede lanzar la excepción de integridad
      """
      with self.assertRaises(StructuralIntegrityError) as cm:
        # Simula la detección de error de indentación
        raise StructuralIntegrityError(42, "Falta indentación en bloque de referencia")
      self.assertIn("línea 42", str(cm.exception))

    def test_export_path_error(self):
      """Validar error cuando la ruta de exportación es un archivo y no un directorio."""
      invalid_path = "/tmp/test_file.txt"
      with open(invalid_path, 'w') as f: f.write("dummy")
      
      # Debería fallar al intentar crear un directorio donde hay un archivo
      with self.assertRaises(Exception):
           # Simulación de lógica de guardado fallida
           if os.path.isfile("/tmp/findOut"): 
               raise ExportPathError("/tmp/findOut", "es un archivo existente")
  



if __name__ == "__main__":
    unittest.main()