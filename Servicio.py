"""
Módulo de Servicio
==================
Define las clases abstracta y concretas para los servicios ofrecidos por Software FJ.
Implementa herencia, polimorfismo y métodos sobrecargados para cálculo de costos.

Autor: Equipo Software FJ
Fecha: 2025
"""

from abc import ABC, abstractmethod
from typing import Optional
from Cliente import Entidad
from Excepciones import (
    ServicioInvalidoError,
    ParametroFaltanteError,
    DatosInvalidosError
)
from Logger import Logger


class Servicio(Entidad, ABC):
    """
    Clase abstracta que representa a los servicios ofrecidos por Software FJ.
    
    Define la interfaz común para todos los servicios con métodos para
    calcular costos, describir servicios y validar disponibilidad.
    """
    
    def __init__(self, id_servicio: str, nombre: str, costo_base: float):
        """
        Inicializa un servicio.
        
        Args:
            id_servicio (str): ID único del servicio
            nombre (str): Nombre del servicio
            costo_base (float): Costo base del servicio en pesos
            
        Raises:
            ParametroFaltanteError: Si falta algún parámetro
            ServicioInvalidoError: Si algún parámetro es inválido
        """
        try:
            super().__init__(id_servicio)
            
            if not nombre or not str(nombre).strip():
                raise ParametroFaltanteError("El nombre del servicio es requerido")
            if costo_base is None or costo_base < 0:
                raise ParametroFaltanteError("El costo base debe ser >= 0")
            
            self._nombre = str(nombre).strip()
            self._costo_base = float(costo_base)
            self._disponible = True
            
            if not self.validar():
                raise ServicioInvalidoError(f"Datos inválidos para servicio: {self._nombre}")
            
        except (ParametroFaltanteError, ServicioInvalidoError):
            raise
        except Exception as e:
            logger = Logger()
            logger.registrar_error("ServicioInvalidoError", str(e), e)
            raise ServicioInvalidoError(f"Error al crear servicio: {str(e)}")
    
    @property
    def nombre(self) -> str:
        """Retorna el nombre del servicio."""
        return self._nombre
    
    @property
    def costo_base(self) -> float:
        """Retorna el costo base del servicio."""
        return self._costo_base
    
    @property
    def disponible(self) -> bool:
        """Retorna si el servicio está disponible."""
        return self._disponible
    
    def establecer_disponibilidad(self, disponible: bool) -> None:
        """Establece la disponibilidad del servicio."""
        self._disponible = disponible
        logger = Logger()
        estado = "disponible" if disponible else "no disponible"
        logger.registrar_evento(
            "Cambio de disponibilidad",
            f"Servicio {self.nombre} ahora está {estado}"
        )
    
    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """
        Calcula el costo del servicio (método abstracto a implementar).
        
        Returns:
            float: Costo total del servicio
        """
        pass
    
    @abstractmethod
    def descripcion(self) -> str:
        """
        Retorna descripción detallada del servicio.
        
        Returns:
            str: Descripción del servicio
        """
        pass
    
    def validar(self) -> bool:
        """
        Valida la integridad del servicio.
        
        Returns:
            bool: True si el servicio es válido
        """
        return (len(self._nombre) > 0 and 
                self._costo_base >= 0 and
                isinstance(self._disponible, bool))
    
    def __str__(self) -> str:
        """Retorna representación en string del servicio."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (f"{self.__class__.__name__}(id={self.id}, nombre='{self.nombre}', "
                f"costo=${self.costo_base}, {estado})")


class ReservaSala(Servicio):
    """
    Clase que representa el servicio de reserva de salas.
    
    Hereda de Servicio e implementa polimorfismo para calcular costos
    basados en horas de uso y servicios adicionales.
    """
    
    TARIFA_HORA = 50000  # Costo por hora en pesos
    
    def __init__(self, id_servicio: str, nombre: str = "Reserva de Sala"):
        """
        Inicializa el servicio de reserva de sala.
        
        Args:
            id_servicio (str): ID único del servicio
            nombre (str): Nombre del servicio
        """
        super().__init__(id_servicio, nombre, self.TARIFA_HORA)
    
    def calcular_costo(self, horas: float, con_equipos: bool = False, 
                      con_catering: bool = False) -> float:
        """
        Calcula el costo de la reserva de sala.
        
        Método sobrecargado que permite múltiples variantes de cálculo.
        
        Args:
            horas (float): Número de horas a reservar
            con_equipos (bool): Si incluye equipos adicionales
            con_catering (bool): Si incluye servicio de catering
            
        Returns:
            float: Costo total de la reserva
            
        Raises:
            DatosInvalidosError: Si las horas son inválidas
        """
        try:
            if horas <= 0:
                raise DatosInvalidosError("Las horas deben ser mayor a 0")
            
            costo = self.TARIFA_HORA * horas
            
            if con_equipos:
                costo += 20000  # Costo adicional por equipos
            if con_catering:
                costo += 30000  # Costo adicional por catering
            
            return costo
            
        except DatosInvalidosError as e:
            logger = Logger()
            logger.registrar_error("DatosInvalidosError", str(e), e)
            raise
    
    def descripcion(self) -> str:
        """Retorna descripción del servicio de reserva de sala."""
        return (f"Reserva de sala profesional - Tarifa: ${self.TARIFA_HORA}/hora. "
                f"Incluye: Aire acondicionado, Proyector. "
                f"Opcionales: Equipos adicionales ($20,000), Catering ($30,000)")
    
    def __str__(self) -> str:
        """Retorna representación en string."""
        return super().__str__()


class AlquilerEquipos(Servicio):
    """
    Clase que representa el servicio de alquiler de equipos.
    
    Implementa polimorfismo para cálculo de costos por días y
    tipos de equipos disponibles.
    """
    
    TARIFA_DIA = 100000  # Costo por día en pesos
    TIPOS_EQUIPOS = {
        "laptop": 1.0,
        "proyector": 0.5,
        "sonido": 0.75,
        "completo": 1.5
    }
    
    def __init__(self, id_servicio: str, nombre: str = "Alquiler de Equipos"):
        """
        Inicializa el servicio de alquiler de equipos.
        
        Args:
            id_servicio (str): ID único del servicio
            nombre (str): Nombre del servicio
        """
        super().__init__(id_servicio, nombre, self.TARIFA_DIA)
    
    def calcular_costo(self, dias: float, tipo_equipo: str = "laptop", 
                      cantidad: int = 1, descuento: float = 0.0) -> float:
        """
        Calcula el costo del alquiler de equipos.
        
        Método sobrecargado con múltiples parámetros y descuentos.
        
        Args:
            dias (float): Número de días de alquiler
            tipo_equipo (str): Tipo de equipo ('laptop', 'proyector', 'sonido', 'completo')
            cantidad (int): Cantidad de equipos
            descuento (float): Descuento porcentual (0.0 - 1.0)
            
        Returns:
            float: Costo total con descuento aplicado
            
        Raises:
            DatosInvalidosError: Si parámetros son inválidos
        """
        try:
            if dias <= 0:
                raise DatosInvalidosError("Los días deben ser mayor a 0")
            if cantidad <= 0:
                raise DatosInvalidosError("La cantidad debe ser mayor a 0")
            if tipo_equipo not in self.TIPOS_EQUIPOS:
                raise DatosInvalidosError(
                    f"Tipo de equipo inválido. Disponibles: {list(self.TIPOS_EQUIPOS.keys())}"
                )
            if not (0.0 <= descuento <= 1.0):
                raise DatosInvalidosError("El descuento debe estar entre 0.0 y 1.0")
            
            multiplicador = self.TIPOS_EQUIPOS[tipo_equipo]
            costo = (self.TARIFA_DIA * dias * multiplicador * cantidad)
            costo = costo * (1 - descuento)
            
            return costo
            
        except DatosInvalidosError as e:
            logger = Logger()
            logger.registrar_error("DatosInvalidosError", str(e), e)
            raise
    
    def descripcion(self) -> str:
        """Retorna descripción del servicio de alquiler."""
        tipos_str = ", ".join(self.TIPOS_EQUIPOS.keys())
        return (f"Alquiler de equipos profesionales - Tarifa: ${self.TARIFA_DIA}/día. "
                f"Tipos disponibles: {tipos_str}. Soporte técnico incluido.")
    
    def __str__(self) -> str:
        """Retorna representación en string."""
        return super().__str__()


class AsesoríaEspecializada(Servicio):
    """
    Clase que representa el servicio de asesorías especializadas.
    
    Implementa cálculo de costos por horas, especialidades y niveles
    de expertise con métodos sobrecargados.
    """
    
    ESPECIALIDADES = {
        "desarrollo": 80000,     # Costo por hora
        "diseño": 70000,
        "infraestructura": 90000,
        "seguridad": 100000,
        "consultoría": 85000
    }
    
    def __init__(self, id_servicio: str, nombre: str = "Asesoría Especializada"):
        """
        Inicializa el servicio de asesoría especializada.
        
        Args:
            id_servicio (str): ID único del servicio
            nombre (str): Nombre del servicio
        """
        super().__init__(id_servicio, nombre, 80000)  # Costo base promedio
    
    def calcular_costo(self, horas: float, especialidad: str = "consultoría", 
                      nivel_urgencia: str = "normal", impuesto: float = 0.19) -> float:
        """
        Calcula el costo de la asesoría especializada.
        
        Método sobrecargado con especialidades, urgencia e impuestos.
        
        Args:
            horas (float): Número de horas de asesoría
            especialidad (str): Especialidad requerida
            nivel_urgencia (str): 'normal', 'urgente' o 'muy_urgente'
            impuesto (float): Porcentaje de IVA a aplicar (0.0 - 1.0)
            
        Returns:
            float: Costo total con impuestos incluidos
            
        Raises:
            DatosInvalidosError: Si parámetros son inválidos
        """
        try:
            if horas <= 0:
                raise DatosInvalidosError("Las horas deben ser mayor a 0")
            if especialidad not in self.ESPECIALIDADES:
                raise DatosInvalidosError(
                    f"Especialidad inválida. Disponibles: {list(self.ESPECIALIDADES.keys())}"
                )
            if nivel_urgencia not in ["normal", "urgente", "muy_urgente"]:
                raise DatosInvalidosError(
                    "Urgencia debe ser 'normal', 'urgente' o 'muy_urgente'"
                )
            if not (0.0 <= impuesto <= 1.0):
                raise DatosInvalidosError("El impuesto debe estar entre 0.0 y 1.0")
            
            costo_hora = self.ESPECIALIDADES[especialidad]
            costo = costo_hora * horas
            
            # Aplicar multiplicador de urgencia
            if nivel_urgencia == "urgente":
                costo *= 1.15  # 15% adicional
            elif nivel_urgencia == "muy_urgente":
                costo *= 1.30  # 30% adicional
            
            # Aplicar impuesto
            costo = costo * (1 + impuesto)
            
            return costo
            
        except DatosInvalidosError as e:
            logger = Logger()
            logger.registrar_error("DatosInvalidosError", str(e), e)
            raise
    
    def descripcion(self) -> str:
        """Retorna descripción del servicio de asesoría."""
        especialidades_str = ", ".join(self.ESPECIALIDADES.keys())
        return (f"Asesoría especializada por expertos - "
                f"Especialidades: {especialidades_str}. "
                f"Incluye: Consulta, Análisis, Reporte. "
                f"Niveles de urgencia: normal, urgente, muy_urgente.")
    
    def __str__(self) -> str:
        """Retorna representación en string."""
        return super().__str__()
