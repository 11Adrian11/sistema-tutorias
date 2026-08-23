from abc import ABC, abstractmethod

from ..domain.reserva import Reserva


class INotificador(ABC):
    """Puerto (abstracción) para avisar eventos relevantes de una Reserva.

    ServicioReservas depende de esta interfaz, NUNCA de una
    implementación concreta (DIP). Esto permite añadir nuevos canales
    (SMS, push, Slack...) implementando esta interfaz sin tocar
    ServicioReservas (OCP).
    """

    @abstractmethod
    def notificar(self, reserva: Reserva, mensaje: str) -> None:
        raise NotImplementedError
