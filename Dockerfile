# Estágio de build permanece o mesmo
FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install uv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY pyproject.toml .
RUN uv pip install --no-cache -r pyproject.toml

# Estágio final atualizado
FROM python:3.12-slim

# Instala o NGINX
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN adduser --system --no-create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY mcp_server.py .
COPY health_check_api.py .
COPY start.sh .
# Copia a configuração do NGINX para o local correto
COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /app/start.sh
ENV PATH="/opt/venv/bin:$PATH"
USER appuser

# Expõe apenas a porta do NGINX
EXPOSE 5000

# Inicia o script que levanta os 3 serviços
CMD ["/app/start.sh"]