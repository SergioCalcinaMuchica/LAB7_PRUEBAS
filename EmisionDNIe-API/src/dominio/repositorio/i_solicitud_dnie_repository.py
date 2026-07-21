"""
Módulo: dominio.repositorio
Interfaz (puerto de salida) que define el contrato de persistencia para
SolicitudDNIe. La capa de dominio no conoce la tecnología de
infraestructura (SQLAlchemy, memoria, etc.) que la implementa.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.dominio.modelo.solicitud_dnie import SolicitudDNIe


class ISolicitudDNIeRepository(ABC):

    @abstractmethod
    def crear(self, solicitud: SolicitudDNIe) -> SolicitudDNIe:
        ...

    @abstractmethod
    def buscar_por_id(self, id_solicitud: int) -> Optional[SolicitudDNIe]:
        ...

    @abstractmethod
    def listar(self) -> List[SolicitudDNIe]:
        ...

    @abstractmethod
    def actualizar(self, solicitud: SolicitudDNIe) -> Optional[SolicitudDNIe]:
        ...

    @abstractmethod
    def eliminar(self, id_solicitud: int) -> bool:
        ...
