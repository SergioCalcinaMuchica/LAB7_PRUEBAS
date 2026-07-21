"""
Módulo: presentacion.controladores
Controlador REST (Blueprint Flask) para el recurso "solicitudes-dnie".

Cada operación corresponde a una feature / historia de usuario del
proceso "Emisión de DNI Electrónico":
  - Crear solicitud de DNIe
  - Consultar solicitud de DNIe
  - Listar solicitudes de DNIe
  - Actualizar solicitud de DNIe (incluye transición de estado)
  - Eliminar / cancelar solicitud de DNIe

Diseñado pensando en integración futura con Bonita BPM: respuestas JSON
estables y códigos HTTP explícitos (200/201/400/404) para que un
conector REST de Bonita pueda evaluar el resultado de cada tarea.
"""

from flask import Blueprint, jsonify, request

from src.aplicacion.interfaces.i_solicitud_dnie_service import ISolicitudDNIeService

solicitud_dnie_bp = Blueprint("solicitud_dnie", __name__, url_prefix="/api/solicitudes-dnie")

_service: ISolicitudDNIeService = None


def inicializar_controlador(service: ISolicitudDNIeService) -> None:
    """Inyecta la dependencia del servicio de aplicación (composition root)."""
    global _service
    _service = service


@solicitud_dnie_bp.post("")
def crear_solicitud():
    """Caso de uso: Registrar solicitud de DNIe."""
    datos = request.get_json(silent=True) or {}
    try:
        solicitud = _service.registrar_solicitud(
            dni_ciudadano=datos.get("dni_ciudadano"),
            nombres=datos.get("nombres"),
            apellidos=datos.get("apellidos"),
        )
        return jsonify(solicitud.a_diccionario()), 201
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@solicitud_dnie_bp.get("/<int:id_solicitud>")
def obtener_solicitud(id_solicitud: int):
    """Caso de uso: Consultar solicitud de DNIe por ID."""
    solicitud = _service.obtener_solicitud(id_solicitud)
    if solicitud is None:
        return jsonify({"error": "Solicitud no encontrada"}), 404
    return jsonify(solicitud.a_diccionario()), 200


@solicitud_dnie_bp.get("")
def listar_solicitudes():
    """Caso de uso: Listar todas las solicitudes de DNIe."""
    solicitudes = _service.listar_solicitudes()
    return jsonify([s.a_diccionario() for s in solicitudes]), 200


@solicitud_dnie_bp.put("/<int:id_solicitud>")
def actualizar_solicitud(id_solicitud: int):
    """Caso de uso: Actualizar datos o estado de una solicitud de DNIe."""
    datos = request.get_json(silent=True) or {}
    try:
        solicitud = _service.actualizar_solicitud(id_solicitud, datos)
        if solicitud is None:
            return jsonify({"error": "Solicitud no encontrada"}), 404
        return jsonify(solicitud.a_diccionario()), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@solicitud_dnie_bp.delete("/<int:id_solicitud>")
def eliminar_solicitud(id_solicitud: int):
    """Caso de uso: Eliminar / cancelar una solicitud de DNIe."""
    eliminado = _service.eliminar_solicitud(id_solicitud)
    if not eliminado:
        return jsonify({"error": "Solicitud no encontrada"}), 404
    return "", 204
