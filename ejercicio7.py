from wsgiref.simple_server import make_server
def app(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/":
        respuesta = b"Inicio"
        status = "200 OK"
    elif path == "/saludo":
        respuesta = b"Hola desde WSGI"
        status = "200 OK"
    else:
        respuesta = b"No encontrado"
        status = "404 Not Found"
    headers = [("Content-Type", "text/plain")]
    start_response(status, headers)
    return [respuesta]
server = make_server("localhost", 8000, app)
print("WSGI corriendo en http://localhost:8000")
server.serve_forever()