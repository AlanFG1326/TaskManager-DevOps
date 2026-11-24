import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def crear(client, **kw):
    datos = {"nombre": "Elaborar documentación", "descripcion": "Detalle", "prioridad": "alta"}
    datos.update(kw)
    return client.post("/api/tasks", json=datos)


def test_registro_tarea_ejemplo():
    tarea = {"nombre": "Realizar actividad DevOps", "estado": "Pendiente"}
    assert tarea["nombre"] == "Realizar actividad DevOps"
    assert tarea["estado"] == "Pendiente"


# Operación
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_pagina_principal(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"TaskManager" in r.data
