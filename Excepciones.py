"""
Módulo de Excepciones Personalizadas
=====================================
Define todas las excepciones personalizadas para el sistema de gestión de reservas
de Software FJ, permitiendo manejo granular de errores específicos del dominio.

Autor: Equipo Software FJ
Fecha: 2025
"""


class ErrorSoftwareFJ(Exception):
    """
    Excepción base personalizada para todas las excepciones del sistema.
    
    Esta clase base permite capturar cualquier error relacionado con Software FJ
    de forma específica, diferenciándolo de otros errores de la aplicación.
    """
    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERAL"):
        """
        Inicializa la excepción base.
        
        Args:
            mensaje (str): Descripción del error
            codigo_error (str): Código identificador del error
        """
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(f"[{codigo_error}] {mensaje}")


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Excepción lanzada cuando un cliente no cumple validaciones."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_CLIENTE_INVALIDO")


class ClienteNoEncontradoError(ErrorSoftwareFJ):
    """Excepción lanzada cuando un cliente no existe en el sistema."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_CLIENTE_NO_ENCONTRADO")


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Excepción lanzada cuando un servicio no cumple validaciones."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_SERVICIO_INVALIDO")


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Excepción lanzada cuando un servicio no está disponible."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_SERVICIO_NO_DISPONIBLE")


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Excepción lanzada cuando una reserva no cumple validaciones."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_RESERVA_INVALIDA")


class ReservaNoEncontradaError(ErrorSoftwareFJ):
    """Excepción lanzada cuando una reserva no existe en el sistema."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_RESERVA_NO_ENCONTRADA")


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Excepción lanzada cuando se intenta una operación no permitida."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_OPERACION_NO_PERMITIDA")


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Excepción lanzada cuando hay inconsistencia en cálculos."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_CALCULO_INCONSISTENTE")


class DatosInvalidosError(ErrorSoftwareFJ):
    """Excepción lanzada cuando hay datos inválidos o inconsistentes."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_DATOS_INVALIDOS")


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Excepción lanzada cuando falta un parámetro requerido."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_PARAMETRO_FALTANTE")
