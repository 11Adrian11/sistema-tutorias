from datetime import datetime

from .docente import Docente


class HorarioDisponible:
    """Un bloque de tiempo que un Docente ofrece para tutoría.

    Responsabilidad única: saber si está disponible y proteger esa
    regla (nadie fuera de esta clase puede marcarlo ocupado sin pasar
    por sus propios métodos -> encapsulación real, no solo un flag
    público).
    """

    def __init__(self, id_horario: str, docente: Docente, inicio: datetime, fin: datetime):
        if fin <= inicio:
            raise ValueError("La hora de fin debe ser posterior al inicio")
        self._id = id_horario
        self._docente = docente
        self._inicio = inicio
        self._fin = fin
        self._disponible = True

    @property
    def id(self) -> str:
        return self._id

    @property
    def docente(self) -> Docente:
        return self._docente

    @property
    def inicio(self) -> datetime:
        return self._inicio

    @property
    def fin(self) -> datetime:
        return self._fin

    @property
    def esta_disponible(self) -> bool:
        return self._disponible

    def ocupar(self) -> None:
        if not self._disponible:
            raise ValueError(f"El horario {self._id} ya está ocupado")
        self._disponible = False

    def liberar(self) -> None:
        self._disponible = True

    def __repr__(self) -> str:
        return f"Horario({self._id}, {self._docente.nombre}, {self._inicio:%d/%m %H:%M})"
