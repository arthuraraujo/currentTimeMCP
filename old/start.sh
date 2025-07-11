#!/bin/sh

# Inicia o servidor MCP em segundo plano
echo "Starting MCP server process..."
python /app/mcp_server.py &

# Inicia o NGINX em primeiro plano para manter o container vivo
echo "Starting NGINX reverse proxy on port 5000..."
nginx -g 'daemon off;'

# #!/bin/sh

# # Inicia a API de healthcheck em segundo plano
# echo "Starting health check process on port 5001..."
# python /app/health_check_api.py &

# # Inicia o servidor MCP em segundo plano
# echo "Starting MCP server process on port 8000..."
# python /app/mcp_server.py &

# # Inicia o NGINX em primeiro plano
# # O NGINX agora é o processo principal que mantém o container rodando
# echo "Starting NGINX reverse proxy on port 5000..."
# nginx -g 'daemon off;'