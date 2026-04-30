"""
Módulo de Logging
=================
Sistema centralizado para registrar eventos, errores y operaciones del sistema
de gestión de reservas de Software FJ en archivo de logs.

Autor: Equipo Software FJ
Fecha: 2025
"""

import os
from datetime import datetime
from typing import Optional


class Logger:
    """
    Gestor centralizado de logs para el sistema.
    
    Registra eventos, errores y operaciones importantes del sistema
    en un archivo de log con formato estructurado y timestamps.
    Implementa patrón Singleton para garantizar una única instancia.
    """
    
    _instancia = None
    
    def __new__(cls):
        """Implementa patrón Singleton."""
        if cls._instancia is None:
            cls._instancia = super(Logger, cls).__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self) -> None:
        """Inicializa el logger con archivo de logs."""
        self.archivo_logs = "registro_eventos.log"
        self._crear_archivo_si_no_existe()
    
    def _crear_archivo_si_no_existe(self) -> None:
        """Crea el archivo de logs si no existe."""
        try:
            if not os.path.exists(self.archivo_logs):
                with open(self.archivo_logs, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("REGISTRO DE EVENTOS - SISTEMA SOFTWARE FJ\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Archivo creado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")
        except Exception as e:
            print(f"Error al crear archivo de logs: {e}")
    
    def _obtener_timestamp(self) -> str:
        """Retorna timestamp formateado."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def registrar_evento(self, evento: str, detalles: str = "") -> None:
        """
        Registra un evento normal en el archivo de logs.
        
        Args:
            evento (str): Tipo o nombre del evento
            detalles (str): Detalles adicionales del evento
        """
        try:
            with open(self.archivo_logs, 'a', encoding='utf-8') as f:
                timestamp = self._obtener_timestamp()
                f.write(f"[{timestamp}] INFO - EVENTO: {evento}\n")
                if detalles:
                    f.write(f"  └─ Detalles: {detalles}\n")
                f.write("\n")
        except Exception as e:
            print(f"Error al registrar evento: {e}")
    
    def registrar_error(self, tipo_error: str, mensaje: str, 
                       excepcion: Optional[Exception] = None) -> None:
        """
        Registra un error en el archivo de logs.
        
        Args:
            tipo_error (str): Tipo o categoría del error
            mensaje (str): Descripción del error
            excepcion (Exception, optional): Excepción capturada
        """
        try:
            with open(self.archivo_logs, 'a', encoding='utf-8') as f:
                timestamp = self._obtener_timestamp()
                f.write(f"[{timestamp}] ERROR - {tipo_error}\n")
                f.write(f"  └─ Mensaje: {mensaje}\n")
                if excepcion:
                    f.write(f"  └─ Excepción: {str(excepcion)}\n")
                f.write("\n")
        except Exception as e:
            print(f"Error al registrar error: {e}")
    
    def registrar_operacion(self, operacion: str, estado: str, 
                           detalles: str = "") -> None:
        """
        Registra una operación importante del sistema.
        
        Args:
            operacion (str): Nombre de la operación
            estado (str): Estado de la operación (EXITOSA, FALLIDA, PENDIENTE)
            detalles (str): Detalles de la operación
        """
        try:
            with open(self.archivo_logs, 'a', encoding='utf-8') as f:
                timestamp = self._obtener_timestamp()
                f.write(f"[{timestamp}] OPERACION - {operacion} [{estado}]\n")
                if detalles:
                    f.write(f"  └─ Detalles: {detalles}\n")
                f.write("\n")
        except Exception as e:
            print(f"Error al registrar operación: {e}")
    
    def registrar_validacion(self, componente: str, resultado: bool, 
                            detalles: str = "") -> None:
        """
        Registra el resultado de una validación.
        
        Args:
            componente (str): Componente validado
            resultado (bool): Resultado de la validación
            detalles (str): Detalles adicionales
        """
        try:
            with open(self.archivo_logs, 'a', encoding='utf-8') as f:
                timestamp = self._obtener_timestamp()
                estado = "VÁLIDO" if resultado else "INVÁLIDO"
                f.write(f"[{timestamp}] VALIDACION - {componente} [{estado}]\n")
                if detalles:
                    f.write(f"  └─ Detalles: {detalles}\n")
                f.write("\n")
        except Exception as e:
            print(f"Error al registrar validación: {e}")
    
    def mostrar_resumen(self) -> None:
        """Muestra un resumen del archivo de logs en consola."""
        try:
            if os.path.exists(self.archivo_logs):
                print("\n" + "="*80)
                print("RESUMEN DEL ARCHIVO DE LOGS")
                print("="*80)
                with open(self.archivo_logs, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    print(contenido)
                print("="*80 + "\n")
        except Exception as e:
            print(f"Error al mostrar resumen: {e}")
