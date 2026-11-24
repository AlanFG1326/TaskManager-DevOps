# Operación y monitoreo – TaskManager

## 1. Qué se monitorea
| Aspecto | Cómo se verifica | Criterio |
|---------|------------------|----------|
| Disponibilidad | `GET /health` → `{"status":"ok","database":true}` | HTTP 200 |
| Tiempo de respuesta | Medición de latencia de `/health` y `/api/tasks` | < 500 ms |
| Errores | Logs del servicio (panel de la plataforma) y pestaña Actions | Sin respuestas 5xx |
| Almacenamiento | Crear → consultar → eliminar una tarea de prueba | Los datos persisten |
| Funcionalidades principales | `scripts/verificar_funcionalidad.py` (CRUD + estados) | Todas OK |

## 2. Registro de monitoreo
| Fecha | Entorno | Disponibilidad | Latencia `GET /api/tasks` (50 solicitudes) | Latencia `/health` | Errores | Observaciones |
|-------|---------|----------------|---------------------------------------------|--------------------|---------|---------------|
| 24/11/2026 | Local (flask run) | OK | media 3.5 ms · máx 4.3 ms | 3 ms | 0 | Línea base previa al despliegue |
| _pendiente_ | Producción (URL pública) | | | | | Completar tras el despliegue (ver README) |

## 3. Registro de incidencias
Las incidencias se documentan como GitHub Issues con la plantilla `.github/ISSUE_TEMPLATE/incidencia.md` (fecha de detección, funcionalidad afectada, descripción, evidencia, responsable, solución).

| Issue | Fecha | Funcionalidad | Resumen | Solución |
|-------|-------|---------------|---------|----------|
| #30 | 24/11/2026 | CI | `ModuleNotFoundError` al ejecutar pytest en Actions | `pytest.ini` con `pythonpath = .` |

## 4. Riesgos conocidos para operación
- **SQLite en plataformas gratuitas:** en Render/Railway el disco es efímero; los datos se pierden en cada redeploy o reinicio. Para producción real se requiere un volumen persistente o migrar a PostgreSQL (ver mejora M2).
- **Cold start:** en planes gratuitos la primera petición tras inactividad puede tardar varios segundos.

## 5. Mejoras propuestas para la versión 1.1 / 2.0
| ID | Mejora | Beneficio |
|----|--------|-----------|
| M1 | Autenticación de usuarios y asignación de tareas por responsable | Seguimiento por empleado (problema original de TechSolutions) |
| M2 | Migrar de SQLite a PostgreSQL con volumen persistente | Persistencia real de datos en producción |
| M3 | Filtros de búsqueda por texto, prioridad y fecha límite | Encontrar tareas rápidamente |
| M4 | Fechas límite y notificaciones por correo | Evitar tareas vencidas |
| M5 | Reporte de productividad (tareas terminadas por semana) | Visibilidad para gerencia |
| M6 | Monitoreo externo (UptimeRobot) y logging estructurado | Detección automática de caídas |
| M7 | Pruebas end-to-end con Playwright en el CI | Cubrir la interfaz, no solo la API |

## 6. Planeación de la versión 1.1
Alcance: M3 + M6 + M7 (bajo riesgo, sin cambio de esquema). Versión 2.0: M1 + M2 + M4 + M5.
