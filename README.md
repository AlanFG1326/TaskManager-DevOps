# TaskManager-DevOps

Sistema web para la gestión de tareas. Caso práctico remedial: implementación de las fases de DevOps con GitHub para la empresa ficticia **TechSolutions**.

## Funcionalidades
| Código | Funcionalidad | Endpoint |
|--------|---------------|----------|
| RF01 | Registrar tareas | `POST /api/tasks` |
| RF02 | Consultar tareas | `GET /api/tasks`, `GET /api/tasks/<id>` |
| RF03 | Editar tareas | `PUT /api/tasks/<id>` |
| RF04 | Eliminar tareas | `DELETE /api/tasks/<id>` |
| RF05 | Cambiar estado (pendiente / en proceso / terminada) | `PATCH /api/tasks/<id>/status` |
| RF06 | Asignar prioridad (alta / media / baja) | campo `prioridad` en alta y edición |
| — | Salud del servicio | `GET /health` |

**Stack:** HTML/CSS/JS · Python 3 + Flask · SQLite · Pytest · GitHub Actions.

## Ejecutar en local
```bash
git clone https://github.com/AlanFG1326/TaskManager-DevOps.git
cd TaskManager-DevOps
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app run                                  # http://127.0.0.1:5000
pytest                                               # pruebas unitarias
```
Variable opcional `DATABASE_PATH` para cambiar la ubicación del archivo SQLite.

## Estructura
```
app.py                     Aplicación Flask (API + páginas)
templates/ static/         Interfaz web
tests/test_app.py          Pruebas unitarias (pytest)
scripts/                   Verificación funcional contra una URL
docs/                      Matriz de pruebas, operación y monitoreo, resultados
.github/workflows/ci.yml   Integración continua
.github/workflows/release.yml  Entrega continua (artefacto al publicar un Release)
render.yaml, Procfile      Configuración de despliegue (Render / plataformas tipo Heroku)
```

## Flujo de trabajo DevOps
1. **Plan:** GitHub Issues + GitHub Projects (tablero con Backlog, To Do, In Progress, Review, Done).
2. **Code:** una rama `feature/*` por funcionalidad → Pull Request a `main`.
3. **CI:** cada push/PR ejecuta `pytest` en GitHub Actions.
4. **Test:** matriz de casos en `docs/matriz-pruebas.md`; errores como Issues.
5. **Release:** al publicar un Release (`v1.0.0`) se genera el artefacto `TaskManager-v1`.
6. **Deploy:** Render (`render.yaml`, comando de inicio `gunicorn app:app`).
7. **Operate/Monitor:** `docs/operacion-monitoreo.md`.

## Despliegue
Ver `docs/despliegue.md`.
