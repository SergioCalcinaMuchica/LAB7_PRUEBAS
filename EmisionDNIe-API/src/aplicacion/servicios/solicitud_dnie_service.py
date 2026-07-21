"""
Módulo: aplicacion.servicios
Implementación de los casos de uso de negocio para SolicitudDNIe.
Coordina el dominio con el repositorio (infraestructura) inyectado por
constructor, siguiendo el Principio de Inversión de Dependencias (SOLID).
"""

from typing import List, Optional

from src.aplicacion.interfaces.i_solicitud_dnie_service import ISolicitudDNIeService
from src.dominio.modelo.solicitud_dnie import SolicitudDNIe
from src.dominio.repositorio.i_solicitud_dnie_repository import ISolicitudDNIeRepository


class SolicitudDNIeService(ISolicitudDNIeService):

    def __init__(self, repositorio: ISolicitudDNIeRepository):
        self._repositorio = repositorio

    def registrar_solicitud(self, dni_ciudadano: str, nombres: str, apellidos: str) -> SolicitudDNIe:
        if not dni_ciudadano or len(dni_ciudadano) != 8:
            raise ValueError("dni_ciudadano debe tener 8 dígitos")
        if not nombres or not apellidos:
            raise ValueError("nombres y apellidos son obligatorios")

        solicitud = SolicitudDNIe(
            dni_ciudadano=dni_ciudadano,
            nombres=nombres,
            apellidos=apellidos,
        )
        return self._repositorio.crear(solicitud)

    def obtener_solicitud(self, id_solicitud: int) -> Optional[SolicitudDNIe]:
        return self._repositorio.buscar_por_id(id_solicitud)

    def listar_solicitudes(self) -> List[SolicitudDNIe]:
        return self._repositorio.listar()

    def actualizar_solicitud(self, id_solicitud: int, datos: dict) -> Optional[SolicitudDNIe]:
        solicitud = self._repositorio.buscar_por_id(id_solicitud)
        if solicitud is None:
            return None

        if "nombres" in datos:
            solicitud.nombres = datos["nombres"]
        if "apellidos" in datos:
            solicitud.apellidos = datos["apellidos"]
        if "estado" in datos:
            solicitud.cambiar_estado(datos["estado"])

        return self._repositorio.actualizar(solicitud)

    def eliminar_solicitud(self, id_solicitud: int) -> bool:
        return self._repositorio.eliminar(id_solicitud)
