from abc import ABC, abstractmethod


class Usuario(ABC):
    """Representa a cualquier persona que interactúa con el sistema.

    Es una clase base ABSTRACTA porque 'Usuario' nunca existe por sí
    solo en el dominio: siempre es un Estudiante o un Docente. La
    herencia aquí es válida (relación "es-un" real) porque ambos
    comparten identidad y datos de contacto, pero difieren en su rol
    y comportamiento -> habilita polimorfismo real, no solo reutilizar
    código.
    """

    def __init__(self, id_usuario: str, nombre: str, email: str):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if "@" not in email:
            raise ValueError("Email inválido")
        self._id = id_usuario
        self._nombre = nombre
        self._email = email

    @property
    def id(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> str:
        return self._email

    @abstractmethod
    def rol(self) -> str:
        """Cada subclase define su propio rol (polimorfismo)."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.rol()}({self._nombre})"
