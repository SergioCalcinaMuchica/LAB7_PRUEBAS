"""
Módulo: aplicacion.interfaces
Contrato de la capa de aplicación: coordina los casos de uso del negocio
sobre SolicitudDNIe (crear, buscar, listar, actualizar, eliminar).
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.dominio.modelo.solicitud_dnie import SolicitudDNIe


class ISolicitudDNIeService(ABC):

    @abstractmethod
    def registrar_solicitud(self, dni_ciudadano: str, nombres: str, apellidos: str) -> SolicitudDNIe:
        ...

    @abstractmethod
    def obtener_solicitud(self, id_solicitud: int) -> Optional[SolicitudDNIe]:
        ...

    @abstractmethod
    def listar_solicitudes(self) -> List[SolicitudDNIe]:
        ...

    @abstractmethod
    def actualizar_solicitud(self, id_solicitud: int, datos: dict) -> Optional[SolicitudDNIe]:
        ...

    @abstractmethod
    def eliminar_solicitud(self, id_solicitud: int) -> bool:
        ...
