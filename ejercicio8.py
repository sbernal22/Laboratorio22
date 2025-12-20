from wsgiref.simple_server import make_server
import json

libros = [
    {"id": 1, "titulo": "1984", "autor": "George Orwell", "anio": 1949}
]
def app(environ, start_response):
    metodo = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    if metodo == "GET" and path == "/libros":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(libros).encode()]
    if metodo == "POST" and path == "/libros":
        length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(length)
        if body:
            data = json.loads(body)
        else:
            data = {}
        if libros:
            max_id = max(libro["id"] for libro in libros)
            data["id"] = max_id + 1
        else:
            data["id"] = 1
        libros.append(data)
        start_response("201 Created", [("Content-Type", "application/json")])
        return [json.dumps(data).encode()]

    if metodo == "GET" and path.startswith("/libros/"):
        libro_id = int(path.split("/")[-1])
        libro = None
        for l in libros:
            if l["id"] == libro_id:
                libro = l
                break
        if libro:
            start_response("200 OK", [("Content-Type", "application/json")])
            return [json.dumps(libro).encode()]
        else:
            start_response("404 Not Found", [("Content-Type", "application/json")])
            return [json.dumps({"error": "Libro no encontrado"}).encode()]
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]
server = make_server("localhost", 8000, app)
print("Servidor WSGI en http://localhost:8000")
server.serve_forever()