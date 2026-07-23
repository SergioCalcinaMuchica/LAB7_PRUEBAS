from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EstadoSolicitud(str, Enum):
    REGISTRADA = "REGISTRADA"
    HUELLAS_CAPTURADAS = "HUELLAS_CAPTURADAS"
    FOTO_CAPTURADA = "FOTO_CAPTURADA"
    HABILITADA = "HABILITADA"
    ENTREGADA = "ENTREGADA"
    CANCELADA = "CANCELADA"

    @classmethod
    def valores(cls):
        return [e.value for e in cls]


@dataclass
class SolicitudDNIe:
    dni_ciudadano: str
    nombres: str
    apellidos: str
    id_solicitud: Optional[int] = None
    estado: str = EstadoSolicitud.REGISTRADA.value
    fecha_solicitud: datetime = field(default_factory=datetime.utcnow)
    fecha_entrega: Optional[datetime] = None

    def cambiar_estado(self, nuevo_estado: str) -> None:
        """Aplica una transición de estado validando que sea un valor permitido.

        Regla de dominio: no se puede modificar una solicitud ya ENTREGADA.
        """
        if nuevo_estado not in EstadoSolicitud.valores():
            raise ValueError(f"Estado inválido: {nuevo_estado}")
        if self.estado == EstadoSolicitud.ENTREGADA.value:
            raise ValueError("No se puede modificar una solicitud ya ENTREGADA")

        self.estado = nuevo_estado
        if nuevo_estado == EstadoSolicitud.ENTREGADA.value:
            self.fecha_entrega = datetime.utcnow()

    def a_diccionario(self) -> dict:
        return {
            "id_solicitud": self.id_solicitud,
            "dni_ciudadano": self.dni_ciudadano,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "estado": self.estado,
            "fecha_solicitud": self.fecha_solicitud.isoformat() if self.fecha_solicitud else None,
            "fecha_entrega": self.fecha_entrega.isoformat() if self.fecha_entrega else None,
        }
