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

# Use a porta que preferir, por exemplo, 5000.
EXPOSE 5000

# Executa o uvicorn apontando para a nossa instância principal 'app'.
CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "5000"]