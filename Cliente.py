"""
Módulo de Cliente
=================
Define la clase Cliente que representa a los clientes del sistema de Software FJ
con validaciones rigurosas, encapsulación de datos y manejo de excepciones.

Autor: Equipo Software FJ
Fecha: 2025
"""

import re
from abc import ABC, abstractmethod
from typing import Optional
from Excepciones import (ClienteInvalidoError, DatosInvalidosError, ParametroFaltanteError,)
from Logger import Logger


class Entidad(ABC):
    """
    Clase abstracta base que representa a las entidades principales del sistema.

    Define la interfaz común para todas las entidades (Cliente, Servicio, Reserva)
    que deben ser persistibles y validables.
    """

    def __init__(self, id_entidad: str):
        """
        Inicializa la entidad base.

        Args:
            id_entidad (str): Identificador único de la entidad

        Raises:
            ParametroFaltanteError: Si el ID está vacío
        """
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El ID de la entidad no puede estar vacío")
        self._id = str(id_entidad).strip()

    @property
    def id(self) -> str:
        """Retorna el ID de la entidad."""
        return self._id

    @abstractmethod
    def validar(self) -> bool:
        """
        Valida la integridad de la entidad.

        Returns:
            bool: True si la entidad es válida
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Retorna representación en string de la entidad."""
        pass


class Cliente(Entidad):
    """
    Clase que representa a un cliente de Software FJ.

    Implementa encapsulación completa con validaciones rigurosas para:
    - Correo electrónico válido
    - Teléfono válido
    - Nombre no vacío
    - Datos consistentes
    """

    # Expresión regular para validar emails
    PATRON_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    # Expresión regular para validar teléfonos (10 dígitos)
    PATRON_TELEFONO = r"^\d{10}$"

    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        """
        Inicializa un cliente con validaciones.

        Args:
            id_cliente (str): ID único del cliente
            nombre (str): Nombre completo del cliente
            email (str): Correo electrónico del cliente
            telefono (str): Teléfono de contacto (10 dígitos)

        Raises:
            ClienteInvalidoError: Si algún parámetro es inválido
            ParametroFaltanteError: Si falta algún parámetro requerido
        """
        try:
            super().__init__(id_cliente)

            if not nombre or not str(nombre).strip():
                raise ParametroFaltanteError("El nombre del cliente es requerido")
            if not email or not str(email).strip():
                raise ParametroFaltanteError("El email del cliente es requerido")
            if not telefono or not str(telefono).strip():
                raise ParametroFaltanteError("El teléfono del cliente es requerido")

            self._nombre = str(nombre).strip()
            self._email = str(email).strip()
            self._telefono = str(telefono).strip()

            # Validar los datos
            if not self.validar():
                raise ClienteInvalidoError(
                    f"Datos inválidos para cliente: {self._nombre}"
                )

            logger = Logger()
            logger.registrar_validacion(
                "Cliente", True, f"Cliente {self._nombre} validado correctamente"
            )

        except (ClienteInvalidoError, ParametroFaltanteError):
            raise
        except Exception as e:
            logger = Logger()
            logger.registrar_error("ClienteInvalidoError", str(e), e)
            raise ClienteInvalidoError(f"Error al crear cliente: {str(e)}")

    @property
    def nombre(self) -> str:
        """Retorna el nombre del cliente."""
        return self._nombre

    @property
    def email(self) -> str:
        """Retorna el email del cliente."""
        return self._email

    @property
    def telefono(self) -> str:
        """Retorna el teléfono del cliente."""
        return self._telefono

    def validar(self) -> bool:
        """
        Valida la integridad completa del cliente.

        Returns:
            bool: True si todos los datos son válidos
        """
        # Validar nombre (solo letras, espacios y caracteres comunes)
        if not re.match(r"^[a-záéíóúñA-ZÁÉÍÓÚÑ\s\-]{3,}$", self._nombre):
            return False

        # Validar email
        if not re.match(self.PATRON_EMAIL, self._email):
            return False

        # Validar teléfono
        if not re.match(self.PATRON_TELEFONO, self._telefono):
            return False

        return True

    def actualizar_contacto(self, email: str, telefono: str) -> None:
        """
        Actualiza información de contacto del cliente.

        Args:
            email (str): Nuevo email
            telefono (str): Nuevo teléfono

        Raises:
            DatosInvalidosError: Si los datos son inválidos
        """
        try:
            if not re.match(self.PATRON_EMAIL, email):
                raise DatosInvalidosError(f"Email inválido: {email}")
            if not re.match(self.PATRON_TELEFONO, telefono):
                raise DatosInvalidosError(f"Teléfono inválido: {telefono}")

            self._email = email
            self._telefono = telefono

            logger = Logger()
            logger.registrar_evento(
                "Actualización de contacto",
                f"Cliente {self._nombre} - Email: {email}, Teléfono: {telefono}",
            )

        except DatosInvalidosError as e:
            logger = Logger()
            logger.registrar_error("DatosInvalidosError", str(e), e)
            raise

    def __str__(self) -> str:
        """Retorna representación en string del cliente."""
        return (
            f"Cliente(id={self.id}, nombre='{self.nombre}', "
            f"email='{self.email}', telefono='{self.telefono}')"
        )

    def __repr__(self) -> str:
        """Retorna representación técnica del cliente."""
        return self.__str__()
