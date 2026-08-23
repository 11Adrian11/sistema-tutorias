from ..domain.reserva import Reserva
from .notificador import INotificador


class EmailNotificador(INotificador):
    """Implementación concreta que simula el envío de un correo.

    En un sistema real aquí se integraría un proveedor SMTP/API de
    correo. El resto del sistema no conoce este detalle: solo conoce
    INotificador (bajo acoplamiento con la tecnología de envío).
    """

    def notificar(self, reserva: Reserva, mensaje: str) -> None:
        destinatario = reserva.estudiante.email
        print(f"[EMAIL -> {destinatario}] {mensaje}")
