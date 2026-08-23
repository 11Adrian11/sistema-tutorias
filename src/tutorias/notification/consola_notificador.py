from ..domain.reserva import Reserva
from .notificador import INotificador


class ConsolaNotificador(INotificador):
    """Segunda implementación de INotificador (ej: para pruebas o modo debug).

    Su sola existencia demuestra Open/Closed Principle: se agregó un
    canal de notificación nuevo sin modificar ni una línea de
    ServicioReservas ni de INotificador.
    """

    def notificar(self, reserva: Reserva, mensaje: str) -> None:
        print(f"[CONSOLA] Reserva {reserva.id}: {mensaje}")
