from wsgiref.simple_server import make_server
import json
import os
equipos = [
    {"id": 1, "nombre": "Real Madrid", "ciudad": "Madrid", "nivelAtaque": 10, "nivelDefensa": 9},
    {"id": 2, "nombre": "Barcelona", "ciudad": "Barcelona", "nivelAtaque": 9, "nivelDefensa": 8},
    {"id": 3, "nombre": "Melgar", "ciudad": "Arequipa", "nivelAtaque": 5, "nivelDefensa": 4}
]
def app(environ, start_response):
    metodo = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    if path.startswith("/static/"):
        archivo = path[8:]
        ruta_completa = os.path.join("static", archivo)
        if os.path.exists(ruta_completa):
            if archivo.endswith(".html"):
                content_type = "text/html"
            elif archivo.endswith(".css"):
                content_type = "text/css"
            elif archivo.endswith(".js"):
                content_type = "application/javascript"
            else:
                content_type = "text/plain"
            with open(ruta_completa, "rb") as f:
                contenido = f.read()
            start_response("200 OK", [("Content-Type", content_type)])
            return [contenido]
        else:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Archivo no encontrado"]
    if metodo == "GET" and path == "/equipos":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(equipos).encode()]
    if metodo == "POST" and path == "/equipos":
        length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(length)
        if body:
            data = json.loads(body)
        else:
            data = {}
        if equipos:
            max_id = max(equipo["id"] for equipo in equipos)
            data["id"] = max_id + 1
        else:
            data["id"] = 1
        equipos.append(data)
        start_response("201 Created", [("Content-Type", "application/json")])
        return [json.dumps(data).encode()]
    if metodo == "GET" and path.startswith("/equipos/"):
        equipo_id = int(path.split("/")[-1])
        equipo = None
        for e in equipos:
            if e["id"] == equipo_id:
                equipo = e
                break
        if equipo:
            start_response("200 OK", [("Content-Type", "application/json")])
            return [json.dumps(equipo).encode()]
        else:
            start_response("404 Not Found", [("Content-Type", "application/json")])
            return [json.dumps({"error": "Equipo no encontrado"}).encode()]
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]
server = make_server("localhost", 8000, app)
print("Servidor corriendo en http://localhost:8000")
server.serve_forever()