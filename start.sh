#!/bin/sh

# Garante que o script pare se algum comando falhar
set -e

# Inicia o servidor de healthcheck em background
echo "Iniciando o servidor de healthcheck na porta 8001..."
python3 -m healthcheck.server &

# Inicia o servidor MCP de tempo em background
echo "Iniciando o servidor MCP na porta 8002..."
python3 -m mcp_simple_timeserver.web.server &

# Inicia o proxy reverso em foreground.
# Isso mantém o contêiner ativo e roteia o tráfego para os outros serviços.
echo "Iniciando o proxy reverso na porta 8000..."
exec python3 -m proxy.server