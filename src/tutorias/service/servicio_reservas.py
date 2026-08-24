import uuid

from ..domain.estado_reserva import EstadoReserva
from ..domain.estudiante import Estudiante
from ..domain.horario_disponible import HorarioDisponible
from ..domain.reserva import Reserva
from ..notification.notificador import INotificador
from .repositorio_reservas import IRepositorioReservas


class ServicioReservas:
    """Orquesta el caso de uso completo de reservas de tutoría.

    Responsabilidad única: coordinar (no *contener*) las reglas de
    negocio. Las reglas de estado viven en Reserva; la disponibilidad
    vive en HorarioDisponible; este servicio solo los hace colaborar.

    Recibe sus dependencias (repositorio y notificador) por
    constructor, como ABSTRACCIONES (IRepositorioReservas,
    INotificador) -> Dependency Inversion Principle: el módulo de
    alto nivel (reglas de negocio) no depende de módulos de bajo
    nivel (email, base de datos), ambos dependen de interfaces.
    """

    def __init__(self, repositorio: IRepositorioReservas, notificador: INotificador):
        self._repositorio = repositorio
        self._notificador = notificador

    def solicitar_reserva(self, estudiante: Estudiante, horario: HorarioDisponible) -> Reserva:
        if not horario.esta_disponible:
            raise ValueError(f"El horario {horario.id} no está disponible")

        horario.ocupar()
        reserva = Reserva(id_reserva=str(uuid.uuid4())[:8], estudiante=estudiante, horario=horario)
        estudiante.registrar_reserva(reserva.id)
        self._repositorio.guardar(reserva)
        self._notificador.notificar(reserva, "Tu solicitud de tutoría fue registrada (PENDIENTE).")
        return reserva

    def confirmar(self, reserva_id: str) -> Reserva:
        reserva = self._obtener_o_fallar(reserva_id)
        reserva.cambiar_estado(EstadoReserva.CONFIRMADA)
        self._repositorio.guardar(reserva)
        self._notificador.notificar(reserva, "Tu tutoría fue confirmada.")
        return reserva

    def cancelar(self, reserva_id: str) -> Reserva:
        reserva = self._obtener_o_fallar(reserva_id)
        reserva.cambiar_estado(EstadoReserva.CANCELADA)
        reserva.horario.liberar()
        self._repositorio.guardar(reserva)
        self._notificador.notificar(reserva, "Tu tutoría fue cancelada.")
        return reserva

    def reprogramar(self, reserva_id: str, nuevo_horario: HorarioDisponible) -> Reserva:
        reserva = self._obtener_o_fallar(reserva_id)
        if not nuevo_horario.esta_disponible:
            raise ValueError(f"El horario {nuevo_horario.id} no está disponible")

        horario_anterior = reserva.horario
        reserva.reprogramar_horario(nuevo_horario)
        reserva.cambiar_estado(EstadoReserva.REPROGRAMADA)
        horario_anterior.liberar()
        nuevo_horario.ocupar()
        self._repositorio.guardar(reserva)
        self._notificador.notificar(reserva, "Tu tutoría fue reprogramada.")
        return reserva

    def _obtener_o_fallar(self, reserva_id: str) -> Reserva:
        reserva = self._repositorio.obtener_por_id(reserva_id)
        if reserva is None:
            raise ValueError(f"No existe la reserva {reserva_id}")
        return reserva
