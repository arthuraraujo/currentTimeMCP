# Estágio de build (sem alterações)
FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install uv
RUN uv venv /opt/venv
COPY pyproject.toml .
RUN uv pip install --no-cache -r pyproject.toml -p /opt/venv/bin/python

# Estágio final
FROM python:3.12-slim

WORKDIR /app

RUN addgroup --system appuser && adduser --system --ingroup appuser --no-create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY mcp_server.py .

ENV PATH="/opt/venv/bin:$PATH"

USER appuser

EXPOSE 5000

# CORREÇÃO FINAL: O comando agora simplesmente executa o script Python,
# que por sua vez chama mcp.run() para iniciar o servidor.
CMD ["python", "mcp_server.py"]