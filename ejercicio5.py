from http.server import BaseHTTPRequestHandler, HTTPServer

class MiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Mi Servidor</title>
            </head>
            <body>
                <h1>Bienvenido</h1>
                <p>Hola en html</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        elif self.path == '/saludo':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"msg": "Hola"}')
server = HTTPServer(("localhost", 8000), MiHandler)
print("Servidor corriendo en http://localhost:8000")
server.serve_forever()