# Matriz de casos de prueba – TaskManager

**Fecha de ejecución:** 24/11/2026 · **Versión probada:** `main` tras PR #29 · **Entorno:** Windows 11, Python 3.14, Flask 3.1 (servidor local `flask run`, SQLite)

## 1. Matriz y resultados

| ID | Prueba | Resultado esperado | Prueba automatizada (pytest) | Ejecución funcional (HTTP real) | Resultado |
|----|--------|--------------------|------------------------------|---------------------------------|-----------|
| CP01 | Registrar una tarea | La tarea se guarda correctamente | `test_cp01_registrar_tarea` | `POST /api/tasks` → 201, tarea con id asignado | Aprobada |
| CP02 | Registrar una tarea sin nombre | El sistema muestra una validación | `test_cp02_registrar_sin_nombre` (vacío, espacios, `null`) | `POST` con nombre vacío → 400 "El nombre de la tarea es obligatorio." | Aprobada |
| CP03 | Consultar tareas | Se muestra el listado | `test_cp03_consultar_tareas` | `GET /api/tasks` → 200, incluye la tarea creada | Aprobada |
| CP04 | Editar una tarea | Se actualiza la información | `test_cp04_editar_tarea` | `PUT /api/tasks/1` → 200, nombre y prioridad actualizados | Aprobada |
| CP05 | Eliminar una tarea | La tarea desaparece del listado | `test_cp05_eliminar_tarea` | `DELETE` → 204; ya no aparece en `GET` | Aprobada |
| CP06 | Cambiar estado | Se actualiza el estado | `test_cp06_cambiar_estado` (3 estados) | `PATCH …/status` con "en proceso", "terminada", "pendiente" → 200 | Aprobada |
| CP07 | Seleccionar prioridad | Se guarda la prioridad elegida | `test_cp07_seleccionar_prioridad` (3 valores) | `POST` con alta/media/baja → 201 con la prioridad enviada | Aprobada |

**Pruebas adicionales (negativas / operación):** nombre > 100 caracteres, prioridad y estado inválidos, 404 en id inexistente (consultar, editar, eliminar, cambiar estado), cuerpo no JSON, `/health` y página principal.

**Resumen:** 25 pruebas automatizadas aprobadas en local y en GitHub Actions; 12 verificaciones funcionales HTTP aprobadas, 0 fallidas.

## 2. Prueba manual de interfaz (CP01 paso a paso)

Pasos definidos en el documento del remedial. **Pendiente de ejecutar por el equipo en navegador** (requiere capturas de pantalla):

1. Abrir `http://127.0.0.1:5000`.
2. Escribir el nombre "Elaborar documentación".
3. Agregar una descripción.
4. Seleccionar prioridad **Alta**.
5. Pulsar **Guardar tarea** → debe aparecer "Tarea guardada correctamente."
6. Verificar que la tarea aparece en el listado con borde rojo (prioridad alta).

## 3. Errores encontrados

| Issue | Descripción | Estado |
|-------|-------------|--------|
| #30 | CI falló con `ModuleNotFoundError: No module named 'app'` (run 45500019784) | Corregido con `pytest.ini`; CI en verde (run 45500129566) |

No se detectaron defectos funcionales en la aplicación durante la ejecución de CP01–CP07.

## 4. Nota sobre la ejecución
Un primer intento con `curl` en Git Bash devolvió 400 en CP01 porque la consola de Windows envió la "ó" con codificación distinta de UTF-8 (JSON inválido). No es un defecto de la aplicación; las pruebas se repitieron con un script en UTF-8 y aprobaron.
