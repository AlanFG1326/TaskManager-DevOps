# Despliegue en Render (Fase 6)

> Estado: **configuración lista; despliegue pendiente** de que el equipo cree/conecte su cuenta de Render (requiere cuenta y autorización de GitHub del equipo).

## Pasos
1. Crear cuenta en https://render.com e iniciar sesión con GitHub.
2. **New → Blueprint** (usa `render.yaml`) o **New → Web Service** y seleccionar el repositorio `TaskManager-DevOps`. Si el repositorio es privado, autorizar a Render el acceso.
3. Configuración (ya incluida en `render.yaml`):
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Health check path: `/health`
   - Variables de entorno: `PYTHON_VERSION=3.12.8`, `DATABASE_PATH=/tmp/tasks.db`
4. Pulsar **Deploy** y esperar a que el estado sea *Live*.
5. Copiar la URL pública (`https://taskmanager-devops-xxxx.onrender.com`).

## Verificación posterior
```bash
python scripts/verificar_funcionalidad.py https://TU-URL.onrender.com
```
Verifica página principal, registro, edición, eliminación y cambio de estado, y deja los tiempos de respuesta para `docs/operacion-monitoreo.md`.

## Limitación importante
En el plan gratuito el disco es efímero: los datos de SQLite se reinician con cada despliegue. Es aceptable para la demostración; para producción ver la mejora M2.
