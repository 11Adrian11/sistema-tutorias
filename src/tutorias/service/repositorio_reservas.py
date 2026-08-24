from abc import ABC, abstractmethod

from ..domain.reserva import Reserva


class IRepositorioReservas(ABC):
    """Puerto de persistencia (abstracción para DIP).

    La lógica de dominio (ServicioReservas) no sabe si las reservas se
    guardan en memoria, en una base SQL, en un archivo o en la nube:
    solo conoce este contrato. Cambiar de tecnología de persistencia
    implica escribir una nueva clase que implemente esta interfaz,
    sin tocar ServicioReservas ni las clases de dominio.
    """

    @abstractmethod
    def guardar(self, reserva: Reserva) -> None:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, reserva_id: str) -> Reserva | None:
        raise NotImplementedError

    @abstractmethod
    def listar_todas(self) -> list[Reserva]:
        raise NotImplementedError
