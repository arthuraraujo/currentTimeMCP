# Estágio de build
FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install uv
RUN uv venv /opt/venv
COPY pyproject.toml .
RUN uv pip install --no-cache -r pyproject.toml -p /opt/venv/bin/python

# Estágio final
FROM python:3.12-slim

RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN addgroup --system appuser && adduser --system --ingroup appuser --no-create-home appuser
RUN chown -R appuser:appuser /var/lib/nginx /var/log/nginx

COPY --from=builder /opt/venv /opt/venv
COPY mcp_server.py .
COPY nginx.conf /etc/nginx/nginx.conf
COPY start.sh .

RUN chmod +x /app/start.sh
ENV PATH="/opt/venv/bin:$PATH"

USER appuser

EXPOSE 5000

CMD ["/app/start.sh"]