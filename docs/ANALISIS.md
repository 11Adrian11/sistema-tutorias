# Analisis y diseño orientado a objetos — Sistema de gestión de tutorías

## 1. Analisis del dominio

| Elemento / clase candidata | Responsabilidad | Informacion relevante | Reglas / colaboraciones |
|---|---|---|---|
| Estudiante | Solicitar tutorias y mantener su historial de reservas | id, nombre, email, carrera | Solo puede reservar horarios disponibles; colabora con Reserva |
| Docente | Publicar disponibilidad y dictar la tutoría | id, nombre, email, materia | Sus horarios los gestiona el sistema, no directamente el docente |
| HorarioDisponible | Representar un bloque de tiempo ofrecido por un docente | id, docente, inicio, fin, disponible | Solo puede ocuparse si está disponible; se libera al cancelar/reprogramar |
| Reserva | Registrar el encuentro entre estudiante y horario, y su estado | id, estudiante, horario, estado | Solo cambia de estado siguiendo transiciones validas (máquina de estados) |
| EstadoReserva | Enumerar los estados posibles del ciclo de vida de una reserva | PENDIENTE, CONFIRMADA, CANCELADA, REPROGRAMADA, COMPLETADA | Usado por Reserva para validar transiciones |
| ServicioReservas | Orquestar el caso de uso completo (solicitar, confirmar, cancelar, reprogramar) | referencias a repositorio y notificador | Coordina, pero no contiene las reglas de estado ni de disponibilidad |
| INotificador | Abstraer el envío de avisos a los usuarios | — | Implementado por EmailNotificador, ConsolaNotificador |
| IRepositorioReservas | Abstraer la persistencia de reservas | — | Implementado por RepositorioReservasMemoria |

## 2. Diseño orientado a objetos

| Clase | Responsabilidad | Atributos principales | Comportamientos | Colabora con |
|---|---|---|---|---|
| Usuario (abstracta) | Identidad común de toda persona del sistema | id, nombre, email | rol() (abstracto) | Estudiante, Docente |
| Estudiante | Identidad + historial de reservas propio | carrera, reservasIds | registrarReserva() | Reserva |
| Docente | Identidad + materia | materia | — | HorarioDisponible |
| HorarioDisponible | Proteger su propia disponibilidad | inicio, fin, disponible | ocupar(), liberar() | Docente, Reserva |
| Reserva | Dueña única de su estado | estado | cambiarEstado(), reprogramarHorario() | Estudiante, HorarioDisponible, EstadoReserva |
| ServicioReservas | Orquestar el flujo de negocio | repositorio, notificador | solicitarReserva(), confirmar(), cancelar(), reprogramar() | IRepositorioReservas, INotificador, Reserva |
| IRepositorioReservas | Contrato de persistencia | — | guardar(), obtenerPorId(), listarTodas() | RepositorioReservasMemoria |
| INotificador | Contrato de notificación | — | notificar() | EmailNotificador, ConsolaNotificador |

**Encapsulación:** todos los atributos son privados (`_prefijo`) y se exponen solo mediante `@property`. `HorarioDisponible` no permite marcarse ocupado directamente: solo a través de `ocupar()`/`liberar()`, que validan la regla. `Reserva` no permite asignar el estado directamente: solo mediante `cambiar_estado()`, que consulta una tabla de transiciones válidas.

**Herencia vs. composición:**
- Se usó **herencia** entre `Usuario` → `Estudiante`/`Docente` porque existe una relación "es-un" genuina: ambos comparten identidad y datos de contacto, pero cada uno tiene comportamiento propio (`rol()` es polimórfico). No es herencia "por conveniencia".
- Se usó **composición** en `ServicioReservas`, que *tiene* un `IRepositorioReservas` y un `INotificador` en lugar de heredar de ellos. Composición es preferible aquí porque la relación es "usa-a", no "es-un", y permite intercambiar la implementación en tiempo de ejecución (inyección por constructor).
- `Reserva` también compone un `HorarioDisponible` y una referencia a `Estudiante`: una reserva no "es" un horario, "tiene" un horario.

## 3. Cohesion y acoplamiento

**Decisiones que favorecen la cohesión:**
- `Reserva` agrupa únicamente lo relacionado con el ciclo de vida de la reserva (estado, horario asociado) y es la única clase que puede modificar su propio estado mediante `cambiar_estado()`. Esto evita que la regla de transición quede dispersa en `ServicioReservas` o en la interfaz de usuario.
- `HorarioDisponible` es responsable únicamente de saber si está libre u ocupado (`ocupar()`/`liberar()`); no sabe nada de reservas, estudiantes ni notificaciones.
- `ServicioReservas` agrupa solo la orquestación del caso de uso de reservas; no contiene lógica de envío de correos ni de acceso a datos.

**Dependencias que podrían producir alto acoplamiento (y cómo se evitaron):**
- Si `ServicioReservas` importara directamente `EmailNotificador` en vez de `INotificador`, quedaría acoplado a una tecnología de envío concreta (SMTP, API externa). Se aisló mediante la interfaz `INotificador`, inyectada por constructor.
- Si `ServicioReservas` guardara las reservas en un diccionario propio en vez de usar `IRepositorioReservas`, quedaría acoplado a una estrategia de almacenamiento. Se aisló con `IRepositorioReservas`, implementada hoy por `RepositorioReservasMemoria`.
- `Reserva` y `HorarioDisponible` no conocen `ServicioReservas` ni las interfaces de notificación/persistencia: la dependencia va en un solo sentido (bajo acoplamiento, alta cohesión de cada módulo).

**Impacto de un cambio de tecnología:**
- Cambiar de persistencia en memoria a una base de datos (SQL, NoSQL) solo requiere escribir `RepositorioReservasSQL(IRepositorioReservas)` e inyectarla en `ServicioReservas`. Ninguna clase de dominio (`Reserva`, `HorarioDisponible`, `Estudiante`, `Docente`) se modifica.
- Cambiar de notificación por email a SMS o push solo requiere una nueva clase que implemente `INotificador` (como ya se demuestra con `ConsolaNotificador`). `ServicioReservas` no cambia.

## 4. Principios SOLID aplicados

**1. Dependency Inversion Principle (DIP).**
`ServicioReservas`, el módulo de alto nivel que contiene las reglas de negocio, no depende de `EmailNotificador` ni de `RepositorioReservasMemoria` (módulos de bajo nivel), sino de las abstracciones `INotificador` e `IRepositorioReservas`, recibidas por constructor. Esto evita que un cambio de proveedor de correo o de motor de persistencia obligue a modificar la lógica de negocio.

**2. Open/Closed Principle (OCP).**
El sistema está abierto a extensión y cerrado a modificación en el canal de notificación: `ConsolaNotificador` se agregó como una segunda implementación de `INotificador` sin tocar `ServicioReservas` ni `INotificador`. Lo mismo aplicaría para agregar un `SmsNotificador` en el futuro.

**3. Single Responsibility Principle (SRP), como refuerzo.**
`Reserva` solo gestiona su propio estado; `HorarioDisponible` solo gestiona su disponibilidad; `ServicioReservas` solo orquesta; `INotificador`/`IRepositorioReservas` solo definen contratos. Ningún cambio en la regla de "cómo se envía una notificación" obliga a tocar la clase `Reserva`, y viceversa.

## 5. Conclusiones

El diseño separa con claridad tres preocupaciones: **reglas de dominio** (`Reserva`, `HorarioDisponible`, estados válidos), **orquestación del caso de uso** (`ServicioReservas`) e **infraestructura** (persistencia y notificación), conectadas mediante abstracciones (`IRepositorioReservas`, `INotificador`). Esto permite que el sistema evolucione —nuevo canal de notificación, nueva tecnología de persistencia, nuevas reglas de negocio— con un impacto controlado y localizado, que era la pregunta orientadora de la actividad. El principal aprendizaje fue que la cohesión no se logra "por convención de nombres" sino protegiendo el estado dentro del objeto dueño de la regla (caso `Reserva.cambiar_estado`), y que el desacoplamiento real se obtiene inyectando abstracciones, no solo declarando interfaces que nadie usa.