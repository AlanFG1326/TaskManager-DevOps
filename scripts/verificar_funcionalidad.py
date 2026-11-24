"""Verificación funcional (CP01-CP07 + /health) contra una instancia en ejecución.
Uso: python scripts/verificar_funcionalidad.py https://URL-PUBLICA"""
import json, urllib.request, urllib.error, time, sys
B=(sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:5000").rstrip("/")
def call(m, p, body=None):
    d=json.dumps(body).encode("utf-8") if body is not None else None
    r=urllib.request.Request(B+p,data=d,method=m,headers={"Content-Type":"application/json; charset=utf-8"})
    t=time.perf_counter()
    try:
        with urllib.request.urlopen(r) as x: s=x.status; raw=x.read()
    except urllib.error.HTTPError as e: s=e.code; raw=e.read()
    ms=(time.perf_counter()-t)*1000
    try: j=json.loads(raw) if raw else None
    except Exception: j=raw[:40]
    return s,j,ms
res=[]
def chk(id_,desc,cond,detail): res.append((id_,desc,"Aprobada" if cond else "FALLIDA",detail)); print(id_,desc,"OK" if cond else "FAIL",detail)
s,j,ms=call("POST","/api/tasks",{"nombre":"Elaborar documentación","descripcion":"Documento DevOps","prioridad":"alta"})
tid=j["id"]; chk("CP01","Registrar una tarea",s==201 and j["nombre"]=="Elaborar documentación",f"HTTP {s}, id={tid}, {ms:.0f} ms")
s,j,ms=call("POST","/api/tasks",{"nombre":"","descripcion":"x"}); chk("CP02","Registrar una tarea sin nombre",s==400 and "obligatorio" in j["error"],f"HTTP {s}: {j['error']}")
s,j,ms=call("GET","/api/tasks"); chk("CP03","Consultar tareas",s==200 and any(t["id"]==tid for t in j),f"HTTP {s}, {len(j)} tarea(s), {ms:.0f} ms")
s,j,ms=call("PUT",f"/api/tasks/{tid}",{"nombre":"Elaborar documentación v2","descripcion":"Actualizada","prioridad":"media"}); chk("CP04","Editar una tarea",s==200 and j["nombre"].endswith("v2") and j["prioridad"]=="media",f"HTTP {s}")
for e in ["en proceso","terminada","pendiente"]:
    s,j,ms=call("PATCH",f"/api/tasks/{tid}/status",{"estado":e}); ok=s==200 and j["estado"]==e
    chk("CP06","Cambiar estado -> "+e,ok,f"HTTP {s}")
for p in ["alta","media","baja"]:
    s,j,ms=call("POST","/api/tasks",{"nombre":"Prioridad "+p,"prioridad":p}); chk("CP07","Seleccionar prioridad "+p,s==201 and j["prioridad"]==p,f"HTTP {s}, id={j['id']}")
s,j,_=call("GET","/api/tasks"); last=j[0]["id"]
s,_,ms=call("DELETE",f"/api/tasks/{last}"); s2,j2,_=call("GET","/api/tasks")
chk("CP05","Eliminar una tarea",s==204 and all(t["id"]!=last for t in j2),f"HTTP {s}, ya no aparece en el listado")
s,j,ms=call("GET","/health"); chk("OP01","Endpoint /health",s==200 and j["status"]=="ok",f"HTTP {s}, {ms:.0f} ms")
lat=[call("GET","/api/tasks")[2] for _ in range(50)]
print("latencia GET /api/tasks x50: media %.1f ms, max %.1f ms"%(sum(lat)/50,max(lat)))
sys.exit(1 if any(r[2]!="Aprobada" for r in res) else 0)
print("FALLIDAS:",sum(1 for r in res if r[2]!="Aprobada"))
