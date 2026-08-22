from .estado_reserva import EstadoReserva
from .estudiante import Estudiante
from .horario_disponible import HorarioDisponible

# Transiciones válidas: estado_actual -> {estados_permitidos}
_TRANSICIONES_VALIDAS: dict[EstadoReserva, set[EstadoReserva]] = {
    EstadoReserva.PENDIENTE: {EstadoReserva.CONFIRMADA, EstadoReserva.CANCELADA},
    EstadoReserva.CONFIRMADA: {
        EstadoReserva.CANCELADA,
        EstadoReserva.REPROGRAMADA,
        EstadoReserva.COMPLETADA,
    },
    EstadoReserva.REPROGRAMADA: {EstadoReserva.CONFIRMADA, EstadoReserva.CANCELADA},
    EstadoReserva.CANCELADA: set(),
    EstadoReserva.COMPLETADA: set(),
}


class TransicionInvalidaError(Exception):
    """Se lanza cuando se intenta un cambio de estado no permitido."""


class Reserva:
    """Registra el encuentro entre un Estudiante y un HorarioDisponible.

    Responsabilidad única y regla de oro de este diseño: SOLO esta
    clase puede cambiar su propio estado, y solo lo hace siguiendo
    _TRANSICIONES_VALIDAS. Esto es lo que le da alta cohesión:
    ServicioReservas orquesta el caso de uso (busca horario, notifica,
    persiste) pero jamás asigna `reserva._estado = ...` directamente.
    """

    def __init__(self, id_reserva: str, estudiante: Estudiante, horario: HorarioDisponible):
        self._id = id_reserva
        self._estudiante = estudiante
        self._horario = horario
        self._estado = EstadoReserva.PENDIENTE

    @property
    def id(self) -> str:
        return self._id

    @property
    def estudiante(self) -> Estudiante:
        return self._estudiante

    @property
    def horario(self) -> HorarioDisponible:
        return self._horario

    @property
    def estado(self) -> EstadoReserva:
        return self._estado

    def cambiar_estado(self, nuevo_estado: EstadoReserva) -> None:
        permitidos = _TRANSICIONES_VALIDAS[self._estado]
        if nuevo_estado not in permitidos:
            raise TransicionInvalidaError(
                f"No se puede pasar de {self._estado.value} a {nuevo_estado.value}"
            )
        self._estado = nuevo_estado

    def reprogramar_horario(self, nuevo_horario: HorarioDisponible) -> None:
        """Cambia el horario asociado; solo válido si la reserva no está cerrada."""
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.COMPLETADA):
            raise TransicionInvalidaError(
                "No se puede reprogramar una reserva cancelada o completada"
            )
        self._horario = nuevo_horario

    def __repr__(self) -> str:
        return f"Reserva({self._id}, {self._estudiante.nombre}, {self._estado.value})"
