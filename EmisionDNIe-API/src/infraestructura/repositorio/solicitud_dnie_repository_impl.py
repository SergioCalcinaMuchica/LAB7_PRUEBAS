"""
Módulo: infraestructura.repositorio
Implementación concreta de ISolicitudDNIeRepository.

NOTA IMPORTANTE:
Esta implementación usa un diccionario en memoria a modo de "Fake" de base
de datos, tal como sugiere la guía del laboratorio en el punto 6:
  "Durante la implementación, usar dobles de prueba para simular
   componentes ausentes o incompletos (Mocks o Fakes de Bases de Datos)."

Para producción, reemplazar esta clase por una que use
Flask-SQLAlchemy (SQLAlchemyRepositoryImpl) sin tocar la capa de
aplicación ni de dominio, gracias a que ambas dependen únicamente
de la interfaz ISolicitudDNIeRepository.
"""

from itertools import count
from typing import Dict, List, Optional

from src.dominio.modelo.solicitud_dnie import SolicitudDNIe
from src.dominio.repositorio.i_solicitud_dnie_repository import ISolicitudDNIeRepository


class SolicitudDNIeRepositoryImpl(ISolicitudDNIeRepository):

    def __init__(self):
        self._almacen: Dict[int, SolicitudDNIe] = {}
        self._secuencia = count(1)

    def crear(self, solicitud: SolicitudDNIe) -> SolicitudDNIe:
        solicitud.id_solicitud = next(self._secuencia)
        self._almacen[solicitud.id_solicitud] = solicitud
        return solicitud

    def buscar_por_id(self, id_solicitud: int) -> Optional[SolicitudDNIe]:
        return self._almacen.get(id_solicitud)

    def listar(self) -> List[SolicitudDNIe]:
        return list(self._almacen.values())

    def actualizar(self, solicitud: SolicitudDNIe) -> Optional[SolicitudDNIe]:
        if solicitud.id_solicitud not in self._almacen:
            return None
        self._almacen[solicitud.id_solicitud] = solicitud
        return solicitud

    def eliminar(self, id_solicitud: int) -> bool:
        return self._almacen.pop(id_solicitud, None) is not None
