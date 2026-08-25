"""Demo del Sistema de gestion de tutorias.

Ejecutar con:  python src/main.py
"""
from datetime import datetime, timedelta

from tutorias.domain import Docente, Estudiante, HorarioDisponible
from tutorias.notification import EmailNotificador
from tutorias.service import RepositorioReservasMemoria, ServicioReservas


def main() -> None:
    docente = Docente("D1", "Ana Torres", "ana.torres@uees.edu.ec", "Estructuras de Datos")
    estudiante = Estudiante("E1", "Luis Pérez", "luis.perez@uees.edu.ec", "Ing. Software")

    inicio = datetime.now() + timedelta(days=1)
    horario1 = HorarioDisponible("H1", docente, inicio, inicio + timedelta(hours=1))
    horario2 = HorarioDisponible("H2", docente, inicio + timedelta(days=1), inicio + timedelta(days=1, hours=1))

    servicio = ServicioReservas(
        repositorio=RepositorioReservasMemoria(),
        notificador=EmailNotificador(),
    )

    reserva = servicio.solicitar_reserva(estudiante, horario1)
    print("Estado inicial:", reserva.estado)

    servicio.confirmar(reserva.id)
    print("Tras confirmar:", reserva.estado)

    servicio.reprogramar(reserva.id, horario2)
    print("Tras reprogramar:", reserva.estado, "->", reserva.horario)

    servicio.cancelar(reserva.id)
    print("Tras cancelar:", reserva.estado, "- horario2 disponible:", horario2.esta_disponible)


if __name__ == "__main__":
    main()
