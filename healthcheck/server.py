import http.server
import socketserver
import json

# Define a porta para o serviço de healthcheck
PORT = 8001

class HealthCheckHandler(http.server.BaseHTTPRequestHandler):
    """
    Um handler simples para responder a checagens de saúde.
    Responde 200 OK com um JSON para qualquer requisição GET ou POST.
    """
    def _send_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))

    def do_GET(self):
        self._send_response()

    def do_POST(self):
        self._send_response()

    def log_message(self, format, *args):
        # Suprime as mensagens de log para manter o output limpo
        return

def run():
    with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
        print(f"Servidor de Healthcheck rodando na porta {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()