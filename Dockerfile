# Estágio de build
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

# CORREÇÃO FINAL: Definimos HOST e PORT como variáveis de ambiente.
# A biblioteca MCP usará estes valores para configurar seu servidor interno.
ENV HOST="0.0.0.0"
ENV PORT="5000"

USER appuser

# Expõe a porta definida pela variável de ambiente.
EXPOSE 5000

# O comando para iniciar o servidor permanece o mesmo.
CMD ["python", "mcp_server.py"]