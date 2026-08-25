# Sistema de gestión de tutorías

Proyecto academico (UEES · Diseño de Software · UCOM0310 · Ae1) que modela, con
principios de diseño orientado a objetos y SOLID, un sistema para que
estudiantes soliciten tutorías y docentes administren su disponibilidad.

> **Nota:** implementado en **Python** (con autorización del docente),
> en lugar de Java/Maven.

## Descripcion del problema

El sistema debe permitir que estudiantes soliciten tutorías sobre horarios
publicados por docentes, gestionar el ciclo de vida de esas reservas
(pendiente, confirmada, cancelada, reprogramada, completada), notificar
eventos relevantes a los usuarios y persistir la información sin acoplar la
lógica de dominio a una tecnología concreta de almacenamiento o de envío de
notificaciones.

## Clases principales y responsabilidades

| Clase | Responsabilidad |
|---|---|
| `Usuario` (abstracta) | Identidad común (id, nombre, email) |
| `Estudiante` | Solicitar tutorías, mantener su historial |
| `Docente` | Publicar disponibilidad |
| `HorarioDisponible` | Proteger su propia disponibilidad |
| `Reserva` | Dueña única de su estado y sus transiciones válidas |
| `ServicioReservas` | Orquestar el caso de uso (solicitar, confirmar, cancelar, reprogramar) |
| `INotificador` / `IRepositorioReservas` | Abstracciones (puertos) para notificación y persistencia |

Ver justificacion completa en [`docs/ANALISIS.md`](docs/ANALISIS.md).

## Decisiones de diseño relevantes

- **Herencia** `Usuario → Estudiante/Docente`: relación "es-un" real, con
  `rol()` polimórfico.
- **Composición** en `ServicioReservas` (inyecta `IRepositorioReservas` e
  `INotificador` por constructor) y en `Reserva` (tiene un `HorarioDisponible`).
- **Máquina de estados encapsulada**: `Reserva.cambiar_estado()` es el único
  punto que puede modificar el estado, validado contra transiciones
  permitidas — protege la invariante del dominio.

## Principios SOLID aplicados

- **DIP**: `ServicioReservas` depende de `INotificador` e
  `IRepositorioReservas`, nunca de sus implementaciones concretas.
- **OCP**: `ConsolaNotificador` se agregó como canal adicional sin modificar
  `ServicioReservas` ni la interfaz `INotificador`.

Detalle completo en [`docs/ANALISIS.md`](docs/ANALISIS.md).

## Diagrama UML

Ver [`docs/modelo-clases.puml`](docs/modelo-clases.puml) 

## Requisitos

- Python 3.10+
- `pytest` (solo para ejecutar las pruebas)

## Como ejecutar

```bash
# Demo del flujo completo
python src/main.py

# Pruebas
pip install pytest
python -m pytest tests/ -v
```

## Estructura del repositorio

## Estructura del repositorio

```text
sistema-tutorias/
├── docs/
│   ├── ANALISIS.md
│   └── modelo-clases.puml
├── src/
│   ├── tutorias/
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   ├── docente.py
│   │   │   ├── estado_reserva.py
│   │   │   ├── estudiante.py
│   │   │   ├── horario_disponible.py
│   │   │   ├── reserva.py
│   │   │   └── usuario.py
│   │   ├── notification/
│   │   │   ├── __init__.py
│   │   │   ├── consola_notificador.py
│   │   │   ├── email_notificador.py
│   │   │   └── notificador.py
│   │   └── service/
│   │       ├── __init__.py
│   │       ├── repositorio_reservas.py
│   │       ├── repositorio_reservas_memoria.py
│   │       └── servicio_reservas.py
│   └── main.py
├── tests/
│   └── test_servicio_reservas.py
└── README.md


## Declaración de uso de IA

Durante el desarrollo de esta actividad utilicé herramientas de inteligencia artificial (Claude y Gemini,) para: apoyar el diseño inicial de clases, redactar el borrador de la justificación de cohesión/acoplamiento y SOLID, estructurar el control de versiones, y generar el esqueleto de pruebas unitarias. Verifiqué, adapté y ejecuté el código, y puedo explicar y justificar todas las decisiones presentadas.
