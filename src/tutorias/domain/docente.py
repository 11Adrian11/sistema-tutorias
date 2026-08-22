from .usuario import Usuario


class Docente(Usuario):
    """Docente que publica horarios disponibles para tutorías.

    Responsabilidad única: identidad del docente + materia que dicta.
    La publicación real de horarios y validación de disponibilidad
    la coordina ServicioReservas (evita que Docente conozca detalles
    de persistencia o notificación -> bajo acoplamiento).
    """

    def __init__(self, id_usuario: str, nombre: str, email: str, materia: str):
        super().__init__(id_usuario, nombre, email)
        self._materia = materia

    @property
    def materia(self) -> str:
        return self._materia

    def rol(self) -> str:
        return "Docente"
