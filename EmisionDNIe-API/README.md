# EmisionDNIe-API

Servicio REST del caso de uso **"Emisión de DNI Electrónico"**, implementado como parte del
Laboratorio 7 (Implementación de Servicios Web REST basados en BDD).

## Propósito

Exponer las operaciones CRUD de una `SolicitudDNIe` (registro, consulta, listado,
actualización de estado y eliminación), como paso previo a integrar este servicio
como conector REST del proceso de Bonita BPM `Emision_DNI_Electronico-1.0.proc`
en el proyecto final del curso.

## Arquitectura (DDD por capas)

```
src/
├── presentacion/     -> Controladores REST (Flask Blueprints)
├── aplicacion/        -> Servicios / casos de uso (interfaces + implementación)
├── dominio/            -> Entidad SolicitudDNIe + interfaz de repositorio (puerto)
├── infraestructura/    -> Implementación del repositorio (actualmente in-memory,
                            reemplazable por SQLAlchemy sin tocar las demás capas)
└── app.py              -> Composition root (ensambla las capas)
```

## Modelo de dominio

`SolicitudDNIe`: dni_ciudadano, nombres, apellidos, estado, fecha_solicitud, fecha_entrega.

Estados: `REGISTRADA -> HUELLAS_CAPTURADAS -> FOTO_CAPTURADA -> HABILITADA -> ENTREGADA`
(o `CANCELADA`). Estos valores están alineados a las tareas del proceso BPM correspondiente.

## Endpoints

| Caso de uso                     | Método | Ruta                              |
|----------------------------------|--------|------------------------------------|
| Registrar solicitud de DNIe      | POST   | /api/solicitudes-dnie             |
| Consultar solicitud por ID       | GET    | /api/solicitudes-dnie/<id>        |
| Listar solicitudes                | GET    | /api/solicitudes-dnie             |
| Actualizar solicitud (datos/estado)| PUT   | /api/solicitudes-dnie/<id>        |
| Eliminar / cancelar solicitud    | DELETE | /api/solicitudes-dnie/<id>        |

## Cómo ejecutar

```bash
python3 -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# Levantar el servidor (por defecto en :5000)
python3 -m flask --app src.app:crear_app run
```

Probar rápido:

```bash
curl -X POST http://localhost:5000/api/solicitudes-dnie \
  -H "Content-Type: application/json" \
  -d '{"dni_ciudadano":"12345678","nombres":"Juan","apellidos":"Perez"}'
```

## Pruebas de Aceptación (BDD / Postman)

En la carpeta `Pruebas de API/` están:
- `EmisionDNIe.postman_collection.json`
- `EmisionDNIe.postman_environment.json`

Importar ambos en Postman, seleccionar el environment "EmisionDNIe - Local",
levantar el servidor Flask y ejecutar la colección completa (Run Collection).

Cada request está organizado como feature (carpeta) con escenarios Given-When-Then:
- **Given**: precondición, en el script Pre-request.
- **When**: la acción HTTP (el propio request).
- **Then**: resultado esperado, en el script de Tests (post-response) con `pm.test`.

## Próximos pasos (proyecto final)

- Reemplazar `SolicitudDNIeRepositoryImpl` (in-memory) por una implementación con
  Flask-SQLAlchemy sobre una base de datos real.
- Añadir autenticación (Basic Auth o token) para el consumo desde Bonita.
- Registrar este servicio como conector REST en la tarea correspondiente del proceso
  `Emision_DNI_Electronico-1.0.proc`.

## Equipo

_(Completar con nombres e integrantes, y su respectiva contribución/commit)_
