"""
exceptions.py
-------------
Definición de la jerarquía de excepciones personalizadas para el 
procesador Reviewer-RST.
"""

class RSTProcessorError(Exception):
    """Clase base para todas las excepciones del procesador Reviewer-RST."""
    def __init__(self, message="Ha ocurrido un error en el procesamiento de RST"):
        self.message = message
        super().__init__(self.message)


class StructuralIntegrityError(RSTProcessorError):
    """
    Excepción lanzada cuando se detecta un fallo de indentación o una 
    estructura inconsistente en los bloques bibliográficos.
    """
    def __init__(self, line_number, details=None):
        self.line_number = line_number
        self.details = details
        msg = f"Error de integridad estructural en la línea {line_number}"
        if details:
            msg += f": {details}"
        super().__init__(msg)


class ExportPathError(RSTProcessorError):
    """
    Excepción lanzada cuando existen problemas de acceso, permisos o 
    existencia del directorio de exportación (ej. /tmp/findOut).
    """
    def __init__(self, path, reason="no accesible"):
        self.path = path
        msg = f"Error en la ruta de exportación '{path}': {reason}"
        super().__init__(msg)