from flask import Flask

from src.aplicacion.servicios.solicitud_dnie_service import SolicitudDNIeService
from src.infraestructura.repositorio.solicitud_dnie_repository_impl import SolicitudDNIeRepositoryImpl
from src.presentacion.controladores.solicitud_dnie_controller import (
    inicializar_controlador,
    solicitud_dnie_bp,
)


def crear_app() -> Flask:
    app = Flask(__name__)

    # Infraestructura (Fake/in-memory por ahora; reemplazable por SQLAlchemy)
    repositorio = SolicitudDNIeRepositoryImpl()

    # Aplicación
    servicio = SolicitudDNIeService(repositorio)

    # Presentación
    inicializar_controlador(servicio)
    app.register_blueprint(solicitud_dnie_bp)

    @app.get("/health")
    def health():
        return {"status": "UP"}, 200

    return app


if __name__ == "__main__":
    app = crear_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
