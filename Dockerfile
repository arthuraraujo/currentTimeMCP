# Estágio 1: "Builder" - Instala dependências
FROM python:3.12-slim as builder
WORKDIR /app

# Instala o 'uv'
RUN pip install uv

# Cria o ambiente virtual
RUN uv venv /opt/venv

COPY pyproject.toml .

# CORREÇÃO:
# Removemos os ENV do estágio de build e usamos a flag '-p' para apontar
# explicitamente para o interpretador Python correto dentro do venv.
RUN uv pip install --no-cache -r pyproject.toml -p /opt/venv/bin/python

# Estágio final (permanece o mesmo)
FROM python:3.12-slim

# Instala o NGINX
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN adduser --system --no-create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY mcp_server.py .
COPY health_check_api.py .
COPY start.sh .
COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /app/start.sh
ENV PATH="/opt/venv/bin:$PATH"
USER appuser

# Expõe apenas a porta do NGINX
EXPOSE 5000

# Inicia o script que levanta os 3 serviços
CMD ["/app/start.sh"]