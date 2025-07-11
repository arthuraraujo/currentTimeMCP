from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection
import sys

# --- Configuração do Proxy ---
PROXY_PORT = 8000
HEALTHCHECK_TARGET = ('127.0.0.1', 8001)
MCP_SERVER_TARGET = ('127.0.0.1', 8002)
# -----------------------------

class ReverseProxy(BaseHTTPRequestHandler):
    """
    Um proxy reverso HTTP que encaminha requisições baseadas no caminho (path).
    - Requisições para /healthcheck são enviadas para o servidor de healthcheck.
    - Todas as outras requisições são enviadas para o servidor MCP.
    """
    def _get_target(self):
        """Determina o destino com base no caminho da requisição."""
        if self.path.startswith('/healthcheck'):
            return HEALTHCHECK_TARGET
        return MCP_SERVER_TARGET

    def _proxy_request(self):
        """Encaminha a requisição para o servidor de destino e retorna a resposta."""
        target_host, target_port = self._get_target()

        try:
            # Estabelece conexão com o servidor de destino
            conn = HTTPConnection(target_host, target_port, timeout=30)

            # Lê o corpo da requisição, se houver
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            # Encaminha a requisição (método, caminho, corpo, cabeçalhos)
            conn.request(self.command, self.path, body=body, headers=self.headers)
            response = conn.getresponse()

            # Envia a resposta de volta ao cliente original
            self.send_response(response.status)
            for key, value in response.getheaders():
                self.send_header(key, value)
            self.end_headers()

            # Transmite o corpo da resposta
            self.wfile.write(response.read())

            conn.close()

        except Exception as e:
            print(f"Erro no proxy: {e}", file=sys.stderr)
            self.send_error(502, "Erro de Proxy")

    # Mapeia todos os métodos HTTP para a função de proxy
    def do_GET(self):
        self._proxy_request()

    def do_POST(self):
        self._proxy_request()

    def do_HEAD(self):
        self._proxy_request()

    def do_OPTIONS(self):
        self._proxy_request()

def run_proxy():
    server_address = ('', PROXY_PORT)
    httpd = HTTPServer(server_address, ReverseProxy)
    print(f"Proxy Reverso rodando na porta {PROXY_PORT}...")
    print(f"  -> Encaminhando '/healthcheck' para {HEALTHCHECK_TARGET[0]}:{HEALTHCHECK_TARGET[1]}")
    print(f"  -> Encaminhando outras requisições para {MCP_SERVER_TARGET[0]}:{MCP_SERVER_TARGET[1]}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_proxy()