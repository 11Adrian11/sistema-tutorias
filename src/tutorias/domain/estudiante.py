from .usuario import Usuario


class Estudiante(Usuario):
    """Estudiante que solicita tutorias.

    Responsabilidad única: representar al estudiante y su historial
    de reservas asociadas (identidad + colección propia). NO decide
    reglas de disponibilidad ni de negocio de la reserva: eso es
    responsabilidad de ServicioReservas y de Reserva (evita romper
    cohesión metiendo lógica ajena aquí).
    """

    def __init__(self, id_usuario: str, nombre: str, email: str, carrera: str):
        super().__init__(id_usuario, nombre, email)
        self._carrera = carrera
        self._reservas_ids: list[str] = []

    @property
    def carrera(self) -> str:
        return self._carrera

    def registrar_reserva(self, reserva_id: str) -> None:
        self._reservas_ids.append(reserva_id)

    @property
    def reservas_ids(self) -> list[str]:
        return list(self._reservas_ids)  # copia defensiva: protege encapsulación

    def rol(self) -> str:
        return "Estudiante"
