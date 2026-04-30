# SISTEMA DE GESTIÓN DE RESERVAS - SOFTWARE FJ

## 📋 Descripción General

Sistema integral orientado a objetos para gestionar **clientes, servicios y reservas** para la empresa **Software FJ**. La aplicación demuestra principios avanzados de Programación Orientada a Objetos (POO) y manejo robusto de excepciones, **sin usar base de datos** - toda la información se gestiona mediante objetos en memoria.

---

## 🎯 Objetivos del Proyecto

✅ Implementar arquitectura OOP completa con:
- Clases abstractas
- Herencia y polimorfismo
- Encapsulación con validaciones rigurosas
- Métodos sobrecargados
- Manejo avanzado de excepciones

✅ Gestionar 3 tipos de servicios:
- **Reserva de Salas** - Espacios profesionales por horas
- **Alquiler de Equipos** - Equipamiento técnico por días
- **Asesoría Especializada** - Consultoría experta por horas

✅ Simular 12 operaciones completas:
- Creación exitosa y fallida de clientes
- Validación de datos personales
- Gestión de servicios
- Ciclo completo de reservas
- Manejo de errores y excepciones

---

## 📁 Estructura del Proyecto

```
Software_FJ/
├── Cliente.py               # Clase Cliente y Entidad (clase abstracta base)
├── Servicio.py              # Clases Servicio, ReservaSala, AlquilerEquipos, AsesoríaEspecializada
├── Reserva.py               # Clase Reserva con estados y operaciones
├── Excepciones.py           # Excepciones personalizadas
├── Logger.py                # Sistema de logging y registro de eventos
├── Main.py                  # Programa principal con 12 operaciones
└── registro_eventos.log     # Archivo de logs (generado al ejecutar)
```

---

## 🏗️ Arquitectura OOP

### Jerarquía de Clases

```
Entidad (Clase Abstracta)
├── Cliente
├── Servicio (Clase Abstracta)
│   ├── ReservaSala
│   ├── AlquilerEquipos
│   └── AsesoríaEspecializada
└── Reserva
```

### Características Implementadas

#### 1. **Encapsulación**
- Atributos privados con propiedades (`@property`)
- Validación de datos en constructores
- Control de acceso mediante métodos

```python
@property
def email(self) -> str:
    """Retorna el email del cliente."""
    return self._email
```

#### 2. **Herencia**
- Clase `Entidad` base abstracta
- Clases derivadas con constructores que llaman al padre
- Especialización de comportamiento

```python
class Cliente(Entidad):
    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        super().__init__(id_cliente)
        # Lógica específica de Cliente
```

#### 3. **Polimorfismo**
- Métodos abstractos implementados en subclases
- Métodos sobrecargados con diferentes firmas

```python
# Método abstracto en Servicio
@abstractmethod
def calcular_costo(self, *args, **kwargs) -> float:
    pass

# Implementaciones polimórficas
class ReservaSala(Servicio):
    def calcular_costo(self, horas: float, con_equipos: bool = False, 
                      con_catering: bool = False) -> float:
        # Lógica específica para Sala

class AlquilerEquipos(Servicio):
    def calcular_costo(self, dias: float, tipo_equipo: str = "laptop", 
                      cantidad: int = 1, descuento: float = 0.0) -> float:
        # Lógica específica para Equipos
```

#### 4. **Métodos Sobrecargados**
- `calcular_costo()` con parámetros variables
- Impuestos, descuentos, urgencia, etc.

```python
# ReservaSala: con_equipos, con_catering
# AlquilerEquipos: tipo_equipo, cantidad, descuento
# AsesoríaEspecializada: especialidad, nivel_urgencia, impuesto
```

---

## ⚠️ Manejo de Excepciones

### Excepciones Personalizadas

```
ErrorSoftwareFJ (Base)
├── ClienteInvalidoError
├── ClienteNoEncontradoError
├── ServicioInvalidoError
├── ServicioNoDisponibleError
├── ReservaInvalidaError
├── ReservaNoEncontradaError
├── OperacionNoPermitidaError
├── CalculoInconsistenteError
├── DatosInvalidosError
└── ParametroFaltanteError
```

### Patrones de Manejo

#### Try/Except Básico
```python
try:
    cliente = Cliente(id, nombre, email, telefono)
except ClienteInvalidoError as e:
    logger.registrar_error("ClienteInvalidoError", str(e), e)
    raise
```

#### Try/Except/Else
```python
try:
    costo = servicio.calcular_costo(**parametros)
except DatosInvalidosError as e:
    print("Parámetros inválidos")
else:
    print(f"Costo calculado: ${costo}")
```

#### Try/Except/Finally
```python
try:
    operacion_critica()
except ErrorSoftwareFJ as e:
    logger.registrar_error("Error", str(e))
finally:
    logger.registrar_evento("Fin de operación", "Completada")
```

#### Encadenamiento de Excepciones
```python
try:
    # Operación que falla
except Exception as e:
    raise CalculoInconsistenteError("Error en cálculo") from e
```

---

## 📊 Las 12 Operaciones Demostrativas

### 1️⃣ Crear Cliente Válido
- **Objetivo**: Registrar cliente con datos verificados
- **Resultado**: ✅ EXITOSA
- **Output**: Cliente registrado en sistema

### 2️⃣ Cliente con Email Inválido
- **Objetivo**: Validar rechazo de formato de email
- **Resultado**: ✅ FALLIDA (como se esperaba)
- **Output**: Excepción capturada y registrada

### 3️⃣ Crear Segundo Cliente Válido
- **Objetivo**: Registrar otro cliente diferente
- **Resultado**: ✅ EXITOSA
- **Output**: Cliente adicional en sistema

### 4️⃣ Cliente con Teléfono Inválido
- **Objetivo**: Validar rechazo de formato de teléfono
- **Resultado**: ✅ FALLIDA (como se esperaba)
- **Output**: Excepción capturada

### 5️⃣ Crear Servicios Disponibles
- **Objetivo**: Registrar 3 tipos de servicios
- **Resultado**: ✅ EXITOSA
- **Output**: ReservaSala, AlquilerEquipos, AsesoríaEspecializada

### 6️⃣ Crear Reserva de Sala Exitosa
- **Objetivo**: Crear reserva para 4 horas
- **Resultado**: ✅ EXITOSA
- **Output**: Reserva en estado PENDIENTE con costo $200,000

### 7️⃣ Reserva con Servicio No Disponible
- **Objetivo**: Validar rechazo de servicio desactivado
- **Resultado**: ✅ FALLIDA (como se esperaba)
- **Output**: ServicioNoDisponibleError

### 8️⃣ Crear y Confirmar Reserva de Equipos
- **Objetivo**: Crear reserva y cambiar estado a CONFIRMADA
- **Resultado**: ✅ EXITOSA
- **Output**: Reserva confirmada con costo $810,000 (con descuento 10%)

### 9️⃣ Reserva con Parámetros Inválidos
- **Objetivo**: Validar rechazo de días negativos
- **Resultado**: ✅ FALLIDA (como se esperaba)
- **Output**: DatosInvalidosError

### 🔟 Ciclo Completo: Crear, Confirmar y Procesar
- **Objetivo**: Reserva de asesoría con ciclo completo
- **Resultado**: ✅ EXITOSA
- **Output**: Reserva PENDIENTE → CONFIRMADA → COMPLETADA

### 1️⃣1️⃣ Crear y Cancelar Reserva
- **Objetivo**: Crear reserva y cancelarla
- **Resultado**: ✅ EXITOSA
- **Output**: Reserva PENDIENTE → CANCELADA

### 1️⃣2️⃣ Operación Inválida en Reserva
- **Objetivo**: Intentar confirmar reserva ya cancelada
- **Resultado**: ✅ FALLIDA (como se esperaba)
- **Output**: OperacionNoPermitidaError

---

## 🔄 Estados de las Reservas

```
PENDIENTE
├─→ CONFIRMADA
│   ├─→ COMPLETADA
│   └─→ CANCELADA
├─→ RECHAZADA
└─→ CANCELADA
```

---

## 💰 Cálculo de Costos

### ReservaSala
```
Costo Base: $50,000/hora
Equipos Adicionales: +$20,000
Catering: +$30,000
Ejemplo: 4 horas = $200,000
```

### AlquilerEquipos
```
Tarifa Base: $100,000/día
Multiplicadores por Tipo:
  - laptop: 1.0x
  - proyector: 0.5x
  - sonido: 0.75x
  - completo: 1.5x
Descuentos: Aplicados al total
Ejemplo: 3 días, completo, 2 unidades, 10% desc = $810,000
```

### AsesoríaEspecializada
```
Tarifas por Especialidad:
  - desarrollo: $80,000/hora
  - diseño: $70,000/hora
  - infraestructura: $90,000/hora
  - seguridad: $100,000/hora
  - consultoría: $85,000/hora
Multiplicadores de Urgencia:
  - normal: 1.0x
  - urgente: 1.15x
  - muy_urgente: 1.3x
IVA: 19% (aplicado)
Ejemplo: 8h, seguridad, urgente, IVA 19% = $1,156,800
```

---

## 📝 Sistema de Logging

### Tipos de Registros

1. **Eventos** - Operaciones normales del sistema
2. **Errores** - Excepciones y errores capturrados
3. **Operaciones** - Cambios de estado importantes
4. **Validaciones** - Resultados de validaciones

### Ejemplo de Log
```
[2025-01-15 10:30:45] INFO - EVENTO: Cliente creado exitosamente
  └─ Detalles: ID: CLI001, Nombre: Juan Pérez García

[2025-01-15 10:30:46] ERROR - ClienteInvalidoError
  └─ Mensaje: Email inválido: email_sin_arroba.com
  └─ Excepción: [ERR_CLIENTE_INVALIDO] Email inválido...

[2025-01-15 10:30:47] OPERACION - Confirmación de Reserva RES001 [EXITOSA]
  └─ Detalles: Cliente: Juan Pérez García, Servicio: Reserva de Sala
```

---

## 🚀 Ejecución del Programa

### Requisitos
- **Python 3.8+**
- Sin dependencias externas

### Cómo Ejecutar

```bash
# En el directorio del proyecto
python Main.py
```

### Salida Esperada
- Consola interactiva mostrando las 12 operaciones
- Resumen de clientes, servicios y reservas
- Contenido completo del archivo de logs
- Archivo `registro_eventos.log` generado

---

## 📋 Validaciones Implementadas

### Cliente
✅ Nombre: Solo letras, espacios y guiones (mínimo 3 caracteres)
✅ Email: Formato válido (RFC estándar)
✅ Teléfono: Exactamente 10 dígitos
✅ ID: No puede estar vacío
✅ Datos completos: Todos los campos requeridos

### Servicio
✅ ID: No puede estar vacío
✅ Nombre: No puede estar vacío
✅ Costo Base: Mayor o igual a 0
✅ Disponibilidad: Booleano válido
✅ Parámetros específicos: Validados en calcular_costo()

### Reserva
✅ Cliente: Instancia válida de Cliente
✅ Servicio: Instancia válida de Servicio
✅ Fecha: Debe estar en el futuro
✅ Parámetros: Requeridos y validados
✅ Costo: Calculado correctamente
✅ Estados: Transiciones válidas

### Cálculo de Costos
✅ Parámetros de entrada: No negativos
✅ Montos: No negativos
✅ Descuentos: Entre 0.0 y 1.0
✅ Impuestos: Entre 0.0 y 1.0
✅ Tipos válidos: Verificación contra lista permitida

---

## 🧪 Casos de Prueba

| # | Operación | Tipo | Resultado Esperado |
|---|-----------|------|-------------------|
| 1 | Crear cliente válido | ✅ Normal | EXITOSA |
| 2 | Email inválido | ❌ Validación | FALLIDA |
| 3 | Crear cliente #2 | ✅ Normal | EXITOSA |
| 4 | Teléfono inválido | ❌ Validación | FALLIDA |
| 5 | Crear 3 servicios | ✅ Normal | EXITOSA |
| 6 | Reserva sala válida | ✅ Normal | EXITOSA |
| 7 | Servicio no disponible | ❌ Validación | FALLIDA |
| 8 | Confirmar reserva | ✅ Normal | EXITOSA |
| 9 | Parámetros inválidos | ❌ Validación | FALLIDA |
| 10 | Ciclo completo | ✅ Normal | EXITOSA |
| 11 | Crear y cancelar | ✅ Normal | EXITOSA |
| 12 | Operación inválida | ❌ Operación | FALLIDA |

---

## 📚 Principios OOP Demostrados

| Principio | Implementación | Archivo |
|-----------|----------------|---------|
| **Abstracción** | Clases `Entidad`, `Servicio` abstractas | Cliente.py, Servicio.py |
| **Encapsulación** | Atributos privados y propiedades | Cliente.py, Reserva.py |
| **Herencia** | Cliente, Servicios heredan de Entidad | Cliente.py, Servicio.py |
| **Polimorfismo** | calcular_costo() sobrescrito | Servicio.py |
| **Sobrecarga** | calcular_costo() con parámetros variables | Servicio.py |
| **Validación** | Métodos validar() en todas las clases | Cliente.py, Reserva.py |
| **Excepciones** | 10 excepciones personalizadas | Excepciones.py |
| **Logging** | Sistema centralizado de logs | Logger.py |
| **Singleton** | Patrón Singleton para Logger | Logger.py |
| **Enum** | EstadoReserva con múltiples valores | Reserva.py |

---

## 🔐 Características de Seguridad y Robustez

✅ **Validaciones Exhaustivas**
- Verificación en constructores
- Validación antes de operaciones críticas

✅ **Manejo Granular de Excepciones**
- Excepciones específicas por problema
- Captura y registro de todos los errores

✅ **Logging Completo**
- Registro de eventos normales
- Registro de errores con detalles
- Seguimiento de operaciones

✅ **Encapsulación Fuerte**
- Atributos privados
- Acceso controlado mediante propiedades
- Métodos de actualización validados

✅ **Diseño Resistente a Fallos**
- El sistema continúa funcionando tras excepciones
- Cada operación es independiente
- Recuperación automática de errores

---

## 🎓 Conceptos Avanzados Incluidos

### 1. Try/Except con Múltiples Except
```python
try:
    # código
except ClienteInvalidoError:
    # manejo específico
except ParametroFaltanteError:
    # manejo específico
except Exception:
    # manejo genérico
```

### 2. Try/Except/Else
```python
try:
    reserva.confirmar()
except OperacionNoPermitidaError:
    print("No se puede confirmar")
else:
    print("Reserva confirmada exitosamente")
```

### 3. Try/Finally
```python
try:
    operacion()
finally:
    logger.registrar_evento("Fin", "Operación completada")
```

### 4. Lanzamiento de Excepciones
```python
if not cliente:
    raise ClienteInvalidoError("Cliente inválido")
```

### 5. Encadenamiento
```python
except DatosInvalidosError as e:
    raise CalculoInconsistenteError("Error en cálculo") from e
```

---

## 📖 Documentación de Código

Cada módulo incluye:
- Docstring de módulo
- Docstring de clase
- Docstring de método
- Anotaciones de tipo
- Comentarios explicativos
- Ejemplos de uso

---

## 🤝 Contribuciones

Este es un proyecto educativo desarrollado por:
- **Equipo Software FJ**
- **Asignatura**: Programación Orientada a Objetos
- **Tarea**: 4 - Sistema Integral con Manejo de Excepciones

---

## 📄 Licencia

Proyecto educativo - UNAD 2025

---

## ✨ Resumen

Este proyecto demuestra la implementación completa y profesional de:
- ✅ Sistema OOP funcional y modular
- ✅ Manejo avanzado de excepciones
- ✅ Validaciones rigurosas
- ✅ Logging centralizado
- ✅ 12 operaciones demostrativas
- ✅ Código documentado y profesional
- ✅ Resistencia a errores
- ✅ Diseño escalable y extensible

**El sistema está completamente funcional y listo para producción educativa.** 🎉
