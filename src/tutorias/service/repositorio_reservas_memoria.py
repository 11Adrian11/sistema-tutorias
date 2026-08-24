from ..domain.reserva import Reserva
from .repositorio_reservas import IRepositorioReservas


class RepositorioReservasMemoria(IRepositorioReservas):
    """Implementación simple en memoria (dict), útil para demo y pruebas.

    Podría reemplazarse por RepositorioReservasSQL o
    RepositorioReservasArchivo sin que ServicioReservas cambie una
    sola línea (Open/Closed + Dependency Inversion en acción).
    """

    def __init__(self):
        self._datos: dict[str, Reserva] = {}

    def guardar(self, reserva: Reserva) -> None:
        self._datos[reserva.id] = reserva

    def obtener_por_id(self, reserva_id: str) -> Reserva | None:
        return self._datos.get(reserva_id)

    def listar_todas(self) -> list[Reserva]:
        return list(self._datos.values())
