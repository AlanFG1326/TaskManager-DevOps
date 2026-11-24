"""TaskManager - Sistema web para la gestión de tareas (Flask + SQLite)."""
import os
import sqlite3
import time

from flask import Flask, g, jsonify, render_template, request

PRIORIDADES = ("alta", "media", "baja")
ESTADOS = ("pendiente", "en proceso", "terminada")
MAX_NOMBRE = 100
INICIO = time.time()


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DATABASE"] = db_path or os.environ.get(
        "DATABASE_PATH", os.path.join(app.instance_path, "tasks.db")
    )
    os.makedirs(os.path.dirname(app.config["DATABASE"]) or ".", exist_ok=True)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        get_db().execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                prioridad TEXT NOT NULL DEFAULT 'media',
                estado TEXT NOT NULL DEFAULT 'pendiente',
                creada TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        ).connection.commit()

    def error(msg, code=400):
        return jsonify({"error": msg}), code

    def validar(data, parcial=False):
        """Devuelve (datos_limpios, mensaje_error)."""
        if not isinstance(data, dict):
            return None, "El cuerpo debe ser un objeto JSON."
        limpio = {}
        if "nombre" in data or not parcial:
            nombre = data.get("nombre")
            if not isinstance(nombre, str) or not nombre.strip():
                return None, "El nombre de la tarea es obligatorio."
            if len(nombre.strip()) > MAX_NOMBRE:
                return None, f"El nombre no debe exceder {MAX_NOMBRE} caracteres."
            limpio["nombre"] = nombre.strip()
        if "descripcion" in data:
            desc = data["descripcion"]
            if desc is not None and not isinstance(desc, str):
                return None, "La descripción debe ser texto."
            limpio["descripcion"] = (desc or "").strip()
        if "prioridad" in data:
            if data["prioridad"] not in PRIORIDADES:
                return None, "La prioridad debe ser alta, media o baja."
            limpio["prioridad"] = data["prioridad"]
        if "estado" in data:
            if data["estado"] not in ESTADOS:
                return None, "El estado debe ser pendiente, en proceso o terminada."
            limpio["estado"] = data["estado"]
        return limpio, None

    def fila(task_id):
        return get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        try:
            get_db().execute("SELECT 1").fetchone()
            db_ok = True
        except sqlite3.Error:
            db_ok = False
        return jsonify(
            {
                "status": "ok" if db_ok else "error",
                "database": db_ok,
                "uptime_s": round(time.time() - INICIO, 1),
            }
        ), (200 if db_ok else 503)

    @app.get("/api/tasks")
    def listar():
        rows = get_db().execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        return jsonify([dict(r) for r in rows])

    @app.get("/api/tasks/<int:task_id>")
    def obtener(task_id):
        row = fila(task_id)
        return jsonify(dict(row)) if row else error("Tarea no encontrada.", 404)

    @app.post("/api/tasks")
    def crear():
        datos, msg = validar(request.get_json(silent=True))
        if msg:
            return error(msg)
        cur = get_db().execute(
            "INSERT INTO tasks (nombre, descripcion, prioridad) VALUES (?, ?, ?)",
            (datos["nombre"], datos.get("descripcion", ""), datos.get("prioridad", "media")),
        )
        get_db().commit()
        return jsonify(dict(fila(cur.lastrowid))), 201

    @app.put("/api/tasks/<int:task_id>")
    def editar(task_id):
        if not fila(task_id):
            return error("Tarea no encontrada.", 404)
        datos, msg = validar(request.get_json(silent=True), parcial=True)
        if msg:
            return error(msg)
        if datos:
            sets = ", ".join(f"{k} = ?" for k in datos)
            get_db().execute(f"UPDATE tasks SET {sets} WHERE id = ?", (*datos.values(), task_id))
            get_db().commit()
        return jsonify(dict(fila(task_id)))

    @app.delete("/api/tasks/<int:task_id>")
    def eliminar(task_id):
        if not fila(task_id):
            return error("Tarea no encontrada.", 404)
        get_db().execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        get_db().commit()
        return "", 204

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
