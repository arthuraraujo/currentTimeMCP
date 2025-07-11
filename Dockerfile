# =================================================================
# Estágio 1: "Builder" - Instala dependências
# =================================================================
FROM python:3.12-slim as builder

WORKDIR /app

# Instala o 'uv' globalmente no estágio de build
RUN pip install uv

# Cria um ambiente virtual para isolar as dependências
RUN uv venv /opt/venv

# "Ativa" o venv para os próximos comandos RUN
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY pyproject.toml .

# Instala as dependências do projeto no ambiente virtual
RUN uv pip install --no-cache -r pyproject.toml


# =================================================================
# Estágio 2: "Final" - Configura o container de execução
# =================================================================
FROM python:3.12-slim

WORKDIR /app

RUN adduser --system --no-create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY simple_streamable_http_mcp_server.py .

ENV PATH="/opt/venv/bin:$PATH"

USER appuser

EXPOSE 8000

# CORREÇÃO: Uvicorn deve rodar o objeto 'app', que agora é o nosso ponto de entrada principal.
CMD ["uvicorn", "simple_streamable_http_mcp_server:app", "--host", "0.0.0.0", "--port", "5000"]