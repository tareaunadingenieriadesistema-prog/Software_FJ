"""
Módulo de Reserva
=================
Define la clase Reserva que integra clientes, servicios y gestiona
confirmación, cancelación y procesamiento con manejo avanzado de excepciones.

Autor: Equipo Software FJ
Fecha: 2025
"""

from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, List
from Cliente import Entidad, Cliente
from Servicio import Servicio
from Excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametroFaltanteError
)
from Logger import Logger


class EstadoReserva(Enum):
    """Enumeración de los posibles estados de una reserva."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    COMPLETADA = "COMPLETADA"
    RECHAZADA = "RECHAZADA"


class Reserva(Entidad):
    """
    Clase que representa una reserva en el sistema.
    
    Integra cliente, servicio y gestiona el ciclo de vida completo
    de una reserva con validaciones, confirmación y cancelación.
    """
    
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio,
                 fecha_inicio: datetime, parametros_servicio: dict):
        """
        Inicializa una reserva.
        
        Args:
            id_reserva (str): ID único de la reserva
            cliente (Cliente): Cliente que realiza la reserva
            servicio (Servicio): Servicio a reservar
            fecha_inicio (datetime): Fecha y hora de inicio
            parametros_servicio (dict): Parámetros específicos del servicio
            
        Raises:
            ReservaInvalidaError: Si algún parámetro es inválido
            ParametroFaltanteError: Si falta algún parámetro esencial
        """
        try:
            super().__init__(id_reserva)
            
            if not isinstance(cliente, Cliente):
                raise ParametroFaltanteError("El cliente es requerido y debe ser instancia de Cliente")
            if not isinstance(servicio, Servicio):
                raise ParametroFaltanteError("El servicio es requerido y debe ser instancia de Servicio")
            if not isinstance(fecha_inicio, datetime):
                raise ParametroFaltanteError("La fecha de inicio debe ser datetime")
            if not parametros_servicio or not isinstance(parametros_servicio, dict):
                raise ParametroFaltanteError("Los parámetros del servicio son requeridos")
            
            # Validar que el servicio esté disponible
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está disponible"
                )
            
            # Validar que la fecha sea en el futuro
            if fecha_inicio <= datetime.now():
                raise DatosInvalidosError("La fecha de inicio debe ser en el futuro")
            
            self._cliente = cliente
            self._servicio = servicio
            self._fecha_inicio = fecha_inicio
            self._parametros_servicio = parametros_servicio
            self._estado = EstadoReserva.PENDIENTE
            self._fecha_creacion = datetime.now()
            self._costo_total = 0.0
            self._fecha_confirmacion: Optional[datetime] = None
            self._fecha_cancelacion: Optional[datetime] = None
            self._razon_cancelacion: str = ""
            
            # Calcular costo inicial
            try:
                self._calcular_costo()
            except Exception as e:
                raise CalculoInconsistenteError(
                    f"Error al calcular costo de la reserva: {str(e)}"
                )
            
            if not self.validar():
                raise ReservaInvalidaError("Datos inválidos para la reserva")
            
            logger = Logger()
            logger.registrar_validacion(
                "Reserva",
                True,
                f"Reserva {self.id} para cliente {cliente.nombre} validada"
            )
            
        except (ReservaInvalidaError, ParametroFaltanteError, 
                ServicioNoDisponibleError, DatosInvalidosError, 
                CalculoInconsistenteError):
            raise
        except Exception as e:
            logger = Logger()
            logger.registrar_error("ReservaInvalidaError", str(e), e)
            raise ReservaInvalidaError(f"Error al crear reserva: {str(e)}")
    
    @property
    def cliente(self) -> Cliente:
        """Retorna el cliente de la reserva."""
        return self._cliente
    
    @property
    def servicio(self) -> Servicio:
        """Retorna el servicio de la reserva."""
        return self._servicio
    
    @property
    def fecha_inicio(self) -> datetime:
        """Retorna la fecha de inicio de la reserva."""
        return self._fecha_inicio
    
    @property
    def parametros_servicio(self) -> dict:
        """Retorna los parámetros del servicio."""
        return self._parametros_servicio
    
    @property
    def estado(self) -> EstadoReserva:
        """Retorna el estado actual de la reserva."""
        return self._estado
    
    @property
    def costo_total(self) -> float:
        """Retorna el costo total de la reserva."""
        return self._costo_total
    
    def _calcular_costo(self) -> None:
        """
        Calcula el costo de la reserva basado en los parámetros del servicio.
        
        Raises:
            CalculoInconsistenteError: Si hay error en el cálculo
        """
        try:
            costo = self._servicio.calcular_costo(**self._parametros_servicio)
            
            if costo < 0:
                raise CalculoInconsistenteError("El costo calculado no puede ser negativo")
            
            self._costo_total = costo
            
        except CalculoInconsistenteError:
            raise
        except Exception as e:
            raise CalculoInconsistenteError(
                f"Error al calcular costo: {str(e)}"
            )
    
    def confirmar(self) -> bool:
        """
        Confirma la reserva cambiando su estado a CONFIRMADA.
        
        Returns:
            bool: True si la confirmación es exitosa
            
        Raises:
            OperacionNoPermitidaError: Si la operación no es permitida
        """
        try:
            if self._estado != EstadoReserva.PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado {self._estado.value}"
                )
            
            self._estado = EstadoReserva.CONFIRMADA
            self._fecha_confirmacion = datetime.now()
            
            logger = Logger()
            logger.registrar_operacion(
                f"Confirmación de Reserva {self.id}",
                "EXITOSA",
                f"Cliente: {self._cliente.nombre}, "
                f"Servicio: {self._servicio.nombre}, "
                f"Costo: ${self._costo_total}"
            )
            
            return True
            
        except OperacionNoPermitidaError as e:
            logger = Logger()
            logger.registrar_error("OperacionNoPermitidaError", str(e), e)
            raise
    
    def cancelar(self, razon: str = "") -> bool:
        """
        Cancela la reserva cambiando su estado a CANCELADA.
        
        Args:
            razon (str): Razón de la cancelación
            
        Returns:
            bool: True si la cancelación es exitosa
            
        Raises:
            OperacionNoPermitidaError: Si la operación no es permitida
        """
        try:
            # Solo se pueden cancelar reservas pendientes o confirmadas
            if self._estado not in [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]:
                raise OperacionNoPermitidaError(
                    f"No se puede cancelar una reserva en estado {self._estado.value}"
                )
            
            self._estado = EstadoReserva.CANCELADA
            self._fecha_cancelacion = datetime.now()
            self._razon_cancelacion = razon
            
            logger = Logger()
            logger.registrar_operacion(
                f"Cancelación de Reserva {self.id}",
                "EXITOSA",
                f"Razón: {razon if razon else 'No especificada'}"
            )
            
            return True
            
        except OperacionNoPermitidaError as e:
            logger = Logger()
            logger.registrar_error("OperacionNoPermitidaError", str(e), e)
            raise
    
    def procesar(self) -> bool:
        """
        Procesa la reserva si está confirmada.
        
        Returns:
            bool: True si el procesamiento es exitoso
            
        Raises:
            OperacionNoPermitidaError: Si la reserva no está confirmada
        """
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas confirmadas. "
                    f"Estado actual: {self._estado.value}"
                )
            
            self._estado = EstadoReserva.COMPLETADA
            
            logger = Logger()
            logger.registrar_operacion(
                f"Procesamiento de Reserva {self.id}",
                "EXITOSA",
                f"Monto procesado: ${self._costo_total}"
            )
            
            return True
            
        except OperacionNoPermitidaError as e:
            logger = Logger()
            logger.registrar_error("OperacionNoPermitidaError", str(e), e)
            raise
    
    def rechazar(self, razon: str = "") -> bool:
        """
        Rechaza la reserva si está pendiente.
        
        Args:
            razon (str): Razón del rechazo
            
        Returns:
            bool: True si el rechazo es exitoso
            
        Raises:
            OperacionNoPermitidaError: Si no se puede rechazar
        """
        try:
            if self._estado != EstadoReserva.PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"Solo se pueden rechazar reservas pendientes. "
                    f"Estado actual: {self._estado.value}"
                )
            
            self._estado = EstadoReserva.RECHAZADA
            
            logger = Logger()
            logger.registrar_operacion(
                f"Rechazo de Reserva {self.id}",
                "EXITOSA",
                f"Razón: {razon if razon else 'No especificada'}"
            )
            
            return True
            
        except OperacionNoPermitidaError as e:
            logger = Logger()
            logger.registrar_error("OperacionNoPermitidaError", str(e), e)
            raise
    
    def validar(self) -> bool:
        """
        Valida la integridad de la reserva.
        
        Returns:
            bool: True si todos los datos son válidos
        """
        try:
            # Validar que cliente y servicio existan
            if not self._cliente or not self._servicio:
                return False
            
            # Validar que el estado sea válido
            if not isinstance(self._estado, EstadoReserva):
                return False
            
            # Validar que el costo sea válido
            if self._costo_total < 0:
                return False
            
            # Validar que la fecha sea válida
            if self._fecha_inicio <= self._fecha_creacion:
                return False
            
            return True
            
        except Exception:
            return False
    
    def obtener_resumen(self) -> str:
        """
        Retorna un resumen detallado de la reserva.
        
        Returns:
            str: Resumen formateado de la reserva
        """
        resumen = f"""
        ╔══════════════════════════════════════════════════════════════╗
        ║                    RESUMEN DE RESERVA                        ║
        ╠══════════════════════════════════════════════════════════════╣
        ║ ID Reserva:        {self.id:<45}
        ║ Cliente:           {self._cliente.nombre:<45}
        ║ Email Cliente:     {self._cliente.email:<45}
        ║ Servicio:          {self._servicio.nombre:<45}
        ║ Fecha Inicio:      {self._fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'):<45}
        ║ Estado:            {self._estado.value:<45}
        ║ Costo Total:       ${self._costo_total:<44.2f}
        ║ Fecha Creación:    {self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'):<45}
        ║ Confirmación:      {self._fecha_confirmacion.strftime('%Y-%m-%d %H:%M:%S') if self._fecha_confirmacion else 'Pendiente':<45}
        ╚══════════════════════════════════════════════════════════════╝
        """
        return resumen
    
    def __str__(self) -> str:
        """Retorna representación en string de la reserva."""
        return (f"Reserva(id={self.id}, cliente={self._cliente.nombre}, "
                f"servicio={self._servicio.nombre}, estado={self._estado.value}, "
                f"costo=${self._costo_total})")
    
    def __repr__(self) -> str:
        """Retorna representación técnica de la reserva."""
        return self.__str__()
