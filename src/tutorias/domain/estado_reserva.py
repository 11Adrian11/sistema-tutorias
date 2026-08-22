from enum import Enum


class EstadoReserva(Enum):
    """Estados validos del ciclo de vida de una Reserva.

    La transición entre estados NO se decide aquí; las reglas de
    transición viven dentro de la clase Reserva (alta cohesión: el
    objeto que posee el estado es el único responsable de cambiarlo).
    """

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    REPROGRAMADA = "REPROGRAMADA"
    COMPLETADA = "COMPLETADA"
