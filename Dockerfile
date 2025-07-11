# Estágio de build (sem alterações)
FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install uv
RUN uv venv /opt/venv
COPY pyproject.toml .
RUN uv pip install --no-cache -r pyproject.toml -p /opt/venv/bin/python

# Estágio final (com a correção de permissão)
FROM python:3.12-slim

RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cria o usuário
RUN adduser --system --no-create-home appuser

# CORREÇÃO: Dá ao 'appuser' a propriedade dos diretórios que o NGINX precisa escrever.
# Isso deve ser feito DEPOIS de criar o usuário e ANTES de trocar para ele.
RUN chown -R appuser:appuser /var/lib/nginx /var/log/nginx

COPY --from=builder /opt/venv /opt/venv
COPY mcp_server.py .
COPY health_check_api.py .
COPY start.sh .
COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /app/start.sh
ENV PATH="/opt/venv/bin:$PATH"

# Troca para o usuário não-privilegiado
USER appuser

EXPOSE 5000

CMD ["/app/start.sh"]