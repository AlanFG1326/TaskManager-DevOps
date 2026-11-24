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


# CP01
def test_cp01_registrar_tarea(client):
    r = crear(client)
    assert r.status_code == 201
    t = r.get_json()
    assert t["id"] == 1
    assert t["nombre"] == "Elaborar documentación"
    assert t["estado"] == "pendiente"
    assert t["prioridad"] == "alta"


# CP02
@pytest.mark.parametrize("nombre", ["", "   ", None])
def test_cp02_registrar_sin_nombre(client, nombre):
    r = crear(client, nombre=nombre)
    assert r.status_code == 400
    assert "obligatorio" in r.get_json()["error"]


def test_nombre_demasiado_largo(client):
    assert crear(client, nombre="x" * 101).status_code == 400


def test_registrar_sin_descripcion_es_valido(client):
    r = client.post("/api/tasks", json={"nombre": "Sin descripción"})
    assert r.status_code == 201
    assert r.get_json()["descripcion"] == ""
    assert r.get_json()["prioridad"] == "media"


def test_cuerpo_invalido(client):
    assert client.post("/api/tasks", data="no es json").status_code == 400


# CP03
def test_cp03_consultar_tareas(client):
    assert client.get("/api/tasks").get_json() == []
    crear(client, nombre="A")
    crear(client, nombre="B")
    lista = client.get("/api/tasks").get_json()
    assert [t["nombre"] for t in lista] == ["B", "A"]


def test_consultar_tarea_por_id(client):
    crear(client)
    assert client.get("/api/tasks/1").get_json()["nombre"] == "Elaborar documentación"
    assert client.get("/api/tasks/99").status_code == 404


# CP04
def test_cp04_editar_tarea(client):
    crear(client)
    r = client.put("/api/tasks/1", json={"nombre": "Nuevo nombre", "descripcion": "Otra", "prioridad": "baja"})
    assert r.status_code == 200
    t = r.get_json()
    assert (t["nombre"], t["descripcion"], t["prioridad"]) == ("Nuevo nombre", "Otra", "baja")


def test_editar_con_nombre_vacio_falla(client):
    crear(client)
    assert client.put("/api/tasks/1", json={"nombre": " "}).status_code == 400


def test_editar_inexistente(client):
    assert client.put("/api/tasks/5", json={"nombre": "x"}).status_code == 404


# Operación
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_pagina_principal(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"TaskManager" in r.data
