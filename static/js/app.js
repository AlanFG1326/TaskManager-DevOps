const $ = (id) => document.getElementById(id);
const lista = $("lista");
let tareas = [];

function mostrar(texto, tipo) {
  const m = $("mensaje");
  m.textContent = texto;
  m.className = tipo || "";
}

async function api(url, opciones = {}) {
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  if (resp.status === 204) return null;
  const datos = await resp.json();
  if (!resp.ok) throw new Error(datos.error || "Error inesperado.");
  return datos;
}

function render() {
  const filtro = $("filtro").value;
  const visibles = tareas.filter((t) => !filtro || t.estado === filtro);
  lista.innerHTML = "";
  $("vacio").hidden = visibles.length > 0;
  for (const t of visibles) {
    const li = document.createElement("li");
    li.className = `tarea ${t.prioridad} ${t.estado === "terminada" ? "terminada" : ""}`;
    li.dataset.id = t.id;

    const nombre = document.createElement("div");
    nombre.className = "nombre";
    nombre.textContent = t.nombre;
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = `Prioridad: ${t.prioridad} · Estado: ${t.estado}`;
    const desc = document.createElement("div");
    desc.textContent = t.descripcion;

    const fila = document.createElement("div");
    fila.className = "fila";
    const sel = document.createElement("select");
    sel.setAttribute("aria-label", "Cambiar estado");
    for (const e of ["pendiente", "en proceso", "terminada"]) {
      const o = new Option(e, e, false, e === t.estado);
      sel.add(o);
    }
    sel.addEventListener("change", () => cambiarEstado(t.id, sel.value));
    const bEditar = document.createElement("button");
    bEditar.textContent = "Editar";
    bEditar.className = "mini secundario";
    bEditar.addEventListener("click", () => editar(t));
    const bBorrar = document.createElement("button");
    bBorrar.textContent = "Eliminar";
    bBorrar.className = "mini peligro";
    bBorrar.addEventListener("click", () => eliminar(t));
    fila.append(sel, bEditar, bBorrar);

    li.append(nombre, meta, desc, fila);
    lista.append(li);
  }
}

async function cargar() {
  tareas = await api("/api/tasks");
  render();
}

function limpiarFormulario() {
  $("task-form").reset();
  $("task-id").value = "";
  $("form-titulo").textContent = "Nueva tarea";
  $("guardar").textContent = "Guardar tarea";
  $("cancelar").hidden = true;
}

function editar(t) {
  $("task-id").value = t.id;
  $("nombre").value = t.nombre;
  $("descripcion").value = t.descripcion;
  $("prioridad").value = t.prioridad;
  $("form-titulo").textContent = `Editar tarea #${t.id}`;
  $("guardar").textContent = "Actualizar tarea";
  $("cancelar").hidden = false;
  $("nombre").focus();
}

async function cambiarEstado(id, estado) {
  try {
    await api(`/api/tasks/${id}/status`, { method: "PATCH", body: JSON.stringify({ estado }) });
    mostrar("Estado actualizado.", "ok");
    await cargar();
  } catch (e) {
    mostrar(e.message, "error");
  }
}

async function eliminar(t) {
  if (!confirm(`¿Eliminar la tarea "${t.nombre}"?`)) return;
  try {
    await api(`/api/tasks/${t.id}`, { method: "DELETE" });
    mostrar("Tarea eliminada.", "ok");
    await cargar();
  } catch (e) {
    mostrar(e.message, "error");
  }
}

$("task-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const datos = {
    nombre: $("nombre").value,
    descripcion: $("descripcion").value,
    prioridad: $("prioridad").value,
  };
  if (!datos.nombre.trim()) {
    mostrar("El nombre de la tarea es obligatorio.", "error");
    return;
  }
  const id = $("task-id").value;
  try {
    await api(id ? `/api/tasks/${id}` : "/api/tasks", {
      method: id ? "PUT" : "POST",
      body: JSON.stringify(datos),
    });
    mostrar(id ? "Tarea actualizada correctamente." : "Tarea guardada correctamente.", "ok");
    limpiarFormulario();
    await cargar();
  } catch (e) {
    mostrar(e.message, "error");
  }
});

$("cancelar").addEventListener("click", () => {
  limpiarFormulario();
  mostrar("");
});
$("filtro").addEventListener("change", render);

cargar().catch((e) => mostrar(e.message, "error"));
