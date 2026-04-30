"""
Módulo Principal
================
Programa principal que demuestra todas las funcionalidades del sistema
de gestión de reservas de Software FJ con manejo avanzado de excepciones.

Simula 12 operaciones completas incluyendo casos exitosos y fallidos.

Autor: Equipo Software FJ
Fecha: 2025
"""

import sys
from datetime import datetime, timedelta
from Cliente import Cliente
from Servicio import ReservaSala, AlquilerEquipos, AsesoríaEspecializada
from Reserva import Reserva, EstadoReserva
from Logger import Logger
from Excepciones import ErrorSoftwareFJ


class SistemaGestionReservas:
    """
    Sistema centralizado para gestionar el flujo de operaciones
    del sistema de reservas de Software FJ.
    """
    
    def __init__(self):
        """Inicializa el sistema."""
        self.logger = Logger()
        self.clientes: dict = {}
        self.servicios: dict = {}
        self.reservas: dict = {}
        self.operaciones_completadas = 0
    
    def ejecutar_operaciones(self) -> None:
        """Ejecuta todas las operaciones demostrativas del sistema."""
        print("\n" + "="*80)
        print("SISTEMA DE GESTIÓN DE RESERVAS - SOFTWARE FJ")
        print("="*80 + "\n")
        
        # OPERACION 1: Crear cliente válido
        self._operacion_1_crear_cliente_valido()
        
        # OPERACION 2: Intentar crear cliente con email inválido
        self._operacion_2_cliente_email_invalido()
        
        # OPERACION 3: Crear segundo cliente válido
        self._operacion_3_crear_cliente_valido_2()
        
        # OPERACION 4: Intentar crear cliente con teléfono inválido
        self._operacion_4_cliente_telefono_invalido()
        
        # OPERACION 5: Crear servicios disponibles
        self._operacion_5_crear_servicios()
        
        # OPERACION 6: Crear reserva exitosa (Sala)
        self._operacion_6_crear_reserva_sala_exitosa()
        
        # OPERACION 7: Intentar crear reserva con servicio no disponible
        self._operacion_7_reserva_servicio_no_disponible()
        
        # OPERACION 8: Crear y confirmar reserva (Equipos)
        self._operacion_8_crear_confirmar_reserva_equipos()
        
        # OPERACION 9: Intentar crear reserva con parámetros inválidos
        self._operacion_9_reserva_parametros_invalidos()
        
        # OPERACION 10: Crear, confirmar y procesar reserva (Asesoría)
        self._operacion_10_crear_confirmar_procesar_asesoria()
        
        # OPERACION 11: Crear y cancelar reserva
        self._operacion_11_crear_cancelar_reserva()
        
        # OPERACION 12: Intentar operación inválida en reserva
        self._operacion_12_operacion_invalida_reserva()
        
        # Mostrar resumen final
        self._mostrar_resumen_final()
    
    def _operacion_1_crear_cliente_valido(self) -> None:
        """Operación 1: Crear cliente con datos válidos."""
        print("┌─ OPERACION 1: Crear Cliente Válido")
        print("├─ Objetivo: Registrar un cliente con datos válidos")
        
        try:
            cliente = Cliente(
                id_cliente="CLI001",
                nombre="Juan Pérez García",
                email="juan.perez@empresa.com",
                telefono="3012345678"
            )
            self.clientes["CLI001"] = cliente
            self.operaciones_completadas += 1
            
            print("├─ Estado: ✓ EXITOSA")
            print(f"└─ Resultado: {cliente}\n")
            
            self.logger.registrar_evento(
                "Cliente creado exitosamente",
                f"ID: {cliente.id}, Nombre: {cliente.nombre}"
            )
            
        except ErrorSoftwareFJ as e:
            print(f"├─ Estado: ✗ FALLIDA")
            print(f"└─ Error: {e}\n")
            self.logger.registrar_error("OperacionCliente", str(e), e)
    
    def _operacion_2_cliente_email_invalido(self) -> None:
        """Operación 2: Intentar crear cliente con email inválido."""
        print("┌─ OPERACION 2: Cliente con Email Inválido")
        print("├─ Objetivo: Validar rechazo de email incorrecto")
        
        try:
            cliente = Cliente(
                id_cliente="CLI002",
                nombre="María López",
                email="email_sin_arroba.com",  # Email inválido
                telefono="3109876543"
            )
            print("├─ Estado: ✗ NO DEBERÍA HABER LLEGADO AQUÍ")
            print(f"└─ Resultado: {cliente}\n")
            
        except ErrorSoftwareFJ as e:
            self.operaciones_completadas += 1
            print("├─ Estado: ✓ FALLIDA (Como se esperaba)")
            print(f"└─ Error capturado: {e}\n")
            self.logger.registrar_error("EmailInvalido", str(e), e)
        
        except Exception as e:
            print(f"├─ Estado: ✗ ERROR INESPERADO")
            print(f"└─ Excepción: {e}\n")
            self.logger.registrar_error("ExcepcionInesperada", str(e), e)
    
    def _operacion_3_crear_cliente_valido_2(self) -> None:
        """Operación 3: Crear segundo cliente válido."""
        print("┌─ OPERACION 3: Crear Segundo Cliente Válido")
        print("├─ Objetivo: Registrar otro cliente con datos válidos")
        
        try:
            cliente = Cliente(
                id_cliente="CLI003",
                nombre="Carlos Rodríguez",
                email="carlos.rodriguez@empresa.com",
                telefono="3156789012"
            )
            self.clientes["CLI003"] = cliente
            self.operaciones_completadas += 1
            
            print("├─ Estado: ✓ EXITOSA")
            print(f"└─ Resultado: {cliente}\n")
            
            self.logger.registrar_evento(
                "Cliente creado exitosamente",
                f"ID: {cliente.id}, Nombre: {cliente.nombre}"
            )
            
        except ErrorSoftwareFJ as e:
            print(f"├─ Estado: ✗ FALLIDA")
            print(f"└─ Error: {e}\n")
            self.logger.registrar_error("OperacionCliente", str(e), e)
    
    def _operacion_4_cliente_telefono_invalido(self) -> None:
        """Operación 4: Intentar crear cliente con teléfono inválido."""
        print("┌─ OPERACION 4: Cliente con Teléfono Inválido")
        print("├─ Objetivo: Validar rechazo de teléfono incorrecto")
        
        try:
            cliente = Cliente(
                id_cliente="CLI004",
                nombre="Ana González",
                email="ana.gonzalez@empresa.com",
                telefono="123"  # Teléfono inválido (menos de 10 dígitos)
            )
            print("├─ Estado: ✗ NO DEBERÍA HABER LLEGADO AQUÍ")
            
        except ErrorSoftwareFJ as e:
            self.operaciones_completadas += 1
            print("├─ Estado: ✓ FALLIDA (Como se esperaba)")
            print(f"└─ Error capturado: {e}\n")
            self.logger.registrar_error("TelefonoInvalido", str(e), e)
    
    def _operacion_5_crear_servicios(self) -> None:
        """Operación 5: Crear servicios disponibles."""
        print("┌─ OPERACION 5: Crear Servicios Disponibles")
        print("├─ Objetivo: Registrar los tres tipos de servicios")
        
        try:
            # Crear servicio de Reserva de Sala
            servicio1 = ReservaSala(id_servicio="SRV001")
            self.servicios["SRV001"] = servicio1
            
            # Crear servicio de Alquiler de Equipos
            servicio2 = AlquilerEquipos(id_servicio="SRV002")
            self.servicios["SRV002"] = servicio2
            
            # Crear servicio de Asesoría Especializada
            servicio3 = AsesoríaEspecializada(id_servicio="SRV003")
            self.servicios["SRV003"] = servicio3
            
            self.operaciones_completadas += 1
            
            print(f"├─ Servicio 1: {servicio1.nombre}")
            print(f"│  └─ {servicio1.descripcion()}")
            print(f"├─ Servicio 2: {servicio2.nombre}")
            print(f"│  └─ {servicio2.descripcion()}")
            print(f"├─ Servicio 3: {servicio3.nombre}")
            print(f"│  └─ {servicio3.descripcion()}")
            print("├─ Estado: ✓ EXITOSA")
            print(f"└─ Resultado: 3 servicios creados\n")
            
            self.logger.registrar_evento(
                "Servicios creados exitosamente",
                "Se crearon 3 servicios (Sala, Equipos, Asesoría)"
            )
            
        except ErrorSoftwareFJ as e:
            print(f"├─ Estado: ✗ FALLIDA")
            print(f"└─ Error: {e}\n")
            self.logger.registrar_error("CreacionServicios", str(e), e)
    
    def _operacion_6_crear_reserva_sala_exitosa(self) -> None:
        """Operación 6: Crear reserva exitosa de sala."""
        print("┌─ OPERACION 6: Crear Reserva de Sala Exitosa")
        print("├─ Objetivo: Crear reserva válida para 4 horas sin equipos adicionales")
        
        try:
            cliente = self.clientes["CLI001"]
            servicio = self.servicios["SRV001"]
            fecha_inicio = datetime.now() + timedelta(days=5)
            
            parametros = {
                "horas": 4,
                "con_equipos": False,
                "con_catering": False
            }
            
            reserva = Reserva(
                id_reserva="RES001",
                cliente=cliente,
                servicio=servicio,
                fecha_inicio=fecha_inicio,
                parametros_servicio=parametros
            )
            
            self.reservas["RES001"] = reserva
            self.operaciones_completadas += 1
            
            print("├─ Estado: ✓ EXITOSA")
            print(f"├─ Reserva: {reserva}")
            print(f"├─ Costo: ${reserva.costo_total}")
            print(f"├─ Estado: {reserva.estado.value}")
            print(f"└─ Resumen: {reserva.obtener_resumen()}\n")
            
            self.logger.registrar_operacion(
                "Creación de Reserva",
                "EXITOSA",
                f"Reserva {reserva.id} para {cliente.nombre}"
            )
            
        except ErrorSoftwareFJ as e:
            print(f"├─ Estado: ✗ FALLIDA")
            print(f"└─ Error: {e}\n")
            self.logger.registrar_error("CreacionReserva", str(e), e)
    
    def _operacion_7_reserva_servicio_no_disponible(self) -> None:
        """Operación 7: Intentar crear reserva con servicio no disponible."""
        print("┌─ OPERACION 7: Reserva con Servicio No Disponible")
        print("├─ Objetivo: Validar rechazo de servicio desactivado")
        
        try:
            cliente = self.clientes["CLI003"]
            servicio = self.servicios["SRV002"]
            
            # Desactivar el servicio
            servicio.establecer_disponibilidad(False)
            
            fecha_inicio = datetime.now() + timedelta(days=3)
            
            parametros = {
                "dias": 2,
                "tipo_equipo": "laptop",
                "cantidad": 1,
                "descuento": 0.0
            }
            
            reserva = Reserva(
                id_reserva="RES002",
                cliente=cliente,
                servicio=servicio,
                fecha_inicio=fecha_inicio,
                parametros_servicio=parametros
            )
            
            print("├─ Estado: ✗ NO DEBERÍA HABER LLEGADO AQUÍ")
            
        except ErrorSoftwareFJ as e:
            self.operaciones_completadas += 1
            print("├─ Estado: ✓ FALLIDA (Como se esperaba)")
            print(f"└─ Error capturado: {e}\n")
            self.logger.registrar_error("ServicioNoDisponible", str(e), e)
            
            # Reactivar el servicio
            servicio.establecer_disponibilidad(True)
    
    def _operacion_8_crear_confirmar_reserva_equipos(self) -> None:
        """Operación 8: Crear y confirmar reserva de equipos."""
        print("┌─ OPERACION 8: Crear y Confirmar Reserva de Equipos")
        print("├─ Objetivo: Crear reserva y cambiar estado a CONFIRMADA")
        
        try:
            cliente = self.clientes["CLI001"]
            servicio = self.servicios["SRV002"]
            fecha_inicio = datetime.now() + timedelta(days=7)
            
            parametros = {
                "dias": 3,
                "tipo_equipo": "completo",
                "cantidad": 2,
                "descuento": 0.10  # 10% de descuento
            }
            
            reserva = Reserva(
                id_reserva="RES002",
                cliente=cliente,
                servicio=servicio,
                fecha_inicio=fecha_inicio,
                parametros_servicio=parametros
            )
            
            self.reservas["RES002"] = reserva
            
            # Confirmar la reserva
            reserva.confirmar()
            self.operaciones_completadas += 1
            
            print(f"├─ Reserva: {reserva}")
            print(f"├─ Costo: ${reserva.costo_total}")
            print(f"├─ Estado: {reserva.estado.value}")
            print("├─ Estado: ✓ EXITOSA")
            print(f"└─ Acción: Reserva confirmada\n")
            
            self.logger.registrar_operacion(
                "Confirmación de Reserva",
                "EXITOSA",
                f"Reserva {reserva.id} confirmada"
            )
            
        except ErrorSoftwareFJ as e:
            print(f"├─ Estado: ✗ FALLIDA")
            print(f"└─ Error: {e}\n")
            self.logger.registrar_error("OperacionReserva", str(e), e)
    
    def _operacion_9_reserva_parametros_invalidos(self) -> None:
        """Operación 9: Intentar crear reserva con parámetros inválidos."""
        print("┌─ OPERACION 9: Reserva con Parámetros Inválidos")
        print("├─ Objetivo: Validar cálculo con días negativos")
        
        try:
            cliente = self.clientes["CLI003"]
            servicio = self.servicios["SRV002"]
            fecha_inicio = datetime.now() + timedelta(days=5)
            
            # Parámetros inválidos
            parametros = {
                "dias": -1,  # Días negativos (inválido)
                "tipo_equipo": "laptop",
                "cantidad": 1,
                "descuento": 0.0
            }
            
            reserva = Reserva(
                id_reserva="RES003",
                cliente=cliente,
                servicio=servicio,
                fecha_inicio=fecha_inicio,
                parametros_servicio=parametros
            )
            
            print("├─ Estado: ✗ NO DEBERÍA HABER LLEGADO AQUÍ")
            
        except ErrorSoftwareFJ as e:
            self.operaciones_completadas += 1
            print("├─ Estado: ✓ FALLIDA (Como se esperaba)")
            print(f"└─ Error capturado: {e}\n")
            self.logger.registrar_error("ParametrosInvalidos", str(e), e)
    
    def _operacion_10_crear_confirmar_procesar_asesoria(self) -> None:
        """Operación 10: Crear, confirmar y procesar reserva de asesoría."""
        print("┌─ OPERACION 10: Crear, Confirmar y Procesar Asesoría")
        print("├─ Objetivo: Ciclo completo de reserva con procesamiento")
        
        try:
            cliente = self.clientes["CLI003"]
            servicio = self.servicios["SRV003"]
            fecha_inicio = datetime.now() + timedelta(days=2)
            
            parametros = {
                "horas": 8,
                "especialidad": "seguridad",
                "nivel_urgencia": "urgente",
                "impuesto": 0.19
            }
            
            # Crear reserva
            reserva = Reserva(
                id_reserva="RES003",
                cliente=cliente,
                servicio=servicio,
                fecha_inicio=fecha_inicio,
                parametros_servicio=parametros
            )
            
            self.reservas["RES003"] = reserva
            
            print(f"├─ Crear: {reserva}")
            print(f"├─ Costo: ${reserva.costo_total}")
            print(f"├─ Estado venta: {reserva.estado.value}")
            
            # Confirmar
            reserva.confirmar()
            print(f"├─ Confirmar: Éxito - Estado: {reserva.estado.value}")
            
            # Procesar
            reserva.procesar()
            self.operaciones_completadas += 1
            
            print(f"├─ Procesar: Éxito - Estado: {reserva.estado.value}")
            print("├─ Estado: ✓ EXITOSA")
            print(f"└─ Acción: Ciclo completo realizado\n")
            
            self.logger.registrar_operacion(
                "Ciclo Completo de Reserva",
                "EXITOSA",
                f"Reserva {reserva.id} completada exitosamente"
            )
            
        except ErrorSoftwareFJ as e:
            print(f"├─ Estado: ✗ FALLIDA")
            print(f"└─ Error: {e}\n")
            self.logger.registrar_error("CicloReserva", str(e), e)
    
    def _operacion_11_crear_cancelar_reserva(self) -> None:
        """Operación 11: Crear y cancelar una reserva."""
        print("┌─ OPERACION 11: Crear y Cancelar Reserva")
        print("├─ Objetivo: Crear reserva y luego cancelarla")
        
        try:
            cliente = self.clientes["CLI001"]
            servicio = self.servicios["SRV001"]
            fecha_inicio = datetime.now() + timedelta(days=10)
            
            parametros = {
                "horas": 2,
                "con_equipos": True,
                "con_catering": True
            }
            
            # Crear reserva
            reserva = Reserva(
                id_reserva="RES004",
                cliente=cliente,
                servicio=servicio,
                fecha_inicio=fecha_inicio,
                parametros_servicio=parametros
            )
            
            self.reservas["RES004"] = reserva
            
            print(f"├─ Crear: {reserva}")
            print(f"├─ Estado: {reserva.estado.value}")
            
            # Cancelar
            reserva.cancelar("Cliente solicita cancelación")
            self.operaciones_completadas += 1
            
            print(f"├─ Cancelar: Éxito - Razón: Cliente solicita cancelación")
            print(f"├─ Estado: {reserva.estado.value}")
            print("├─ Estado: ✓ EXITOSA")
            print(f"└─ Acción: Reserva cancelada\n")
            
            self.logger.registrar_operacion(
                "Cancelación de Reserva",
                "EXITOSA",
                f"Reserva {reserva.id} cancelada"
            )
            
        except ErrorSoftwareFJ as e:
            print(f"├─ Estado: ✗ FALLIDA")
            print(f"└─ Error: {e}\n")
            self.logger.registrar_error("CancelacionReserva", str(e), e)
    
    def _operacion_12_operacion_invalida_reserva(self) -> None:
        """Operación 12: Intentar operación inválida en reserva."""
        print("┌─ OPERACION 12: Operación Inválida en Reserva")
        print("├─ Objetivo: Intentar confirmar una reserva ya cancelada")
        
        try:
            # Usar la reserva cancelada de la operación 11
            reserva = self.reservas["RES004"]
            
            print(f"├─ Reserva: {reserva}")
            print(f"├─ Estado actual: {reserva.estado.value}")
            print(f"├─ Intentando: Confirmar reserva cancelada...")
            
            # Intentar confirmar una reserva cancelada
            reserva.confirmar()
            
            print("├─ Estado: ✗ NO DEBERÍA HABER LLEGADO AQUÍ")
            
        except ErrorSoftwareFJ as e:
            self.operaciones_completadas += 1
            print("├─ Estado: ✓ FALLIDA (Como se esperaba)")
            print(f"└─ Error capturado: {e}\n")
            self.logger.registrar_error("OperacionInvalida", str(e), e)
    
    def _mostrar_resumen_final(self) -> None:
        """Muestra un resumen final de todas las operaciones."""
        print("\n" + "="*80)
        print("RESUMEN FINAL DEL SISTEMA")
        print("="*80 + "\n")
        
        print(f"┌─ Total de Operaciones Completadas: {self.operaciones_completadas}/12")
        print(f"├─ Clientes Registrados: {len(self.clientes)}")
        print(f"├─ Servicios Disponibles: {len(self.servicios)}")
        print(f"├─ Reservas Created: {len(self.reservas)}")
        
        # Resumen por estado de reserva
        estados_reserva = {}
        for reserva in self.reservas.values():
            estado = reserva.estado.value
            estados_reserva[estado] = estados_reserva.get(estado, 0) + 1
        
        print(f"├─ Reservas por Estado:")
        for estado, cantidad in estados_reserva.items():
            print(f"│  ├─ {estado}: {cantidad}")
        
        ingresos_totales = sum(r.costo_total for r in self.reservas.values())
        print(f"├─ Ingresos Totales Simulados: ${ingresos_totales:.2f}")
        
        # Mostrar archivo de logs
        print(f"\n├─ Archivo de Logs: registro_eventos.log")
        print("└─ Contenido del archivo de logs:\n")
        
        self.logger.mostrar_resumen()
        
        print("="*80)
        print("FIN DEL PROGRAMA - TODAS LAS OPERACIONES COMPLETADAS")
        print("="*80 + "\n")


def main() -> None:
    """Función principal del programa."""
    try:
        print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    SOFTWARE FJ - SISTEMA DE RESERVAS                        ║")
        print("║              Gestión de Clientes, Servicios y Reservas                      ║")
        print("║                                                                              ║")
        print("║  Autor: Equipo Software FJ                                                  ║")
        print("║  Asignatura: Programación Orientada a Objetos                               ║")
        print("║  Tarea: 4 - Sistema Integral con Manejo de Excepciones                     ║")
        print("║  Fecha: 2025                                                                 ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        # Crear y ejecutar el sistema
        sistema = SistemaGestionReservas()
        sistema.ejecutar_operaciones()
        
        print("✓ Sistema ejecutado exitosamente sin interrupciones")
        
    except Exception as e:
        print(f"\n✗ Error crítico en el sistema: {e}")
        logger = Logger()
        logger.registrar_error("ErrorCritico", str(e), e)
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n✗ Programa interrumpido por el usuario")
        sys.exit(0)
    
    finally:
        print("\nGracias por usar Software FJ - Sistema de Reservas")


if __name__ == "__main__":
    main()
