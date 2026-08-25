import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from tutorias.domain import Docente, EstadoReserva, Estudiante, HorarioDisponible, TransicionInvalidaError
from tutorias.notification import ConsolaNotificador
from tutorias.service import RepositorioReservasMemoria, ServicioReservas


def _servicio():
    return ServicioReservas(RepositorioReservasMemoria(), ConsolaNotificador())


def _horario(id_="H1", offset_dias=1):
    docente = Docente("D1", "Ana Torres", "ana@uees.edu.ec", "POO")
    inicio = datetime.now() + timedelta(days=offset_dias)
    return HorarioDisponible(id_, docente, inicio, inicio + timedelta(hours=1))


def _estudiante():
    return Estudiante("E1", "Luis Pérez", "luis@uees.edu.ec", "Software")


def test_solicitar_reserva_deja_pendiente_y_ocupa_horario():
    servicio = _servicio()
    horario = _horario()
    reserva = servicio.solicitar_reserva(_estudiante(), horario)

    assert reserva.estado == EstadoReserva.PENDIENTE
    assert horario.esta_disponible is False


def test_no_se_puede_reservar_horario_ocupado():
    servicio = _servicio()
    horario = _horario()
    servicio.solicitar_reserva(_estudiante(), horario)

    with pytest.raises(ValueError):
        servicio.solicitar_reserva(_estudiante(), horario)


def test_confirmar_cambia_estado():
    servicio = _servicio()
    reserva = servicio.solicitar_reserva(_estudiante(), _horario())

    servicio.confirmar(reserva.id)

    assert reserva.estado == EstadoReserva.CONFIRMADA


def test_no_se_puede_confirmar_una_reserva_cancelada():
    servicio = _servicio()
    reserva = servicio.solicitar_reserva(_estudiante(), _horario())
    servicio.cancelar(reserva.id)

    with pytest.raises(TransicionInvalidaError):
        reserva.cambiar_estado(EstadoReserva.CONFIRMADA)


def test_cancelar_libera_el_horario():
    servicio = _servicio()
    horario = _horario()
    reserva = servicio.solicitar_reserva(_estudiante(), horario)

    servicio.cancelar(reserva.id)

    assert horario.esta_disponible is True
    assert reserva.estado == EstadoReserva.CANCELADA


def test_reprogramar_mueve_la_reserva_a_nuevo_horario():
    servicio = _servicio()
    reserva = servicio.solicitar_reserva(_estudiante(), _horario("H1"))
    servicio.confirmar(reserva.id)
    nuevo_horario = _horario("H2", offset_dias=2)

    servicio.reprogramar(reserva.id, nuevo_horario)

    assert reserva.estado == EstadoReserva.REPROGRAMADA
    assert reserva.horario.id == "H2"
    assert nuevo_horario.esta_disponible is False
