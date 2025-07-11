# =================================================================
# Estágio 1: "Builder" - Instala dependências
# =================================================================
FROM python:3.12-slim as builder

WORKDIR /app

# Instala o 'uv' globalmente no estágio de build
RUN pip install uv

# Cria um ambiente virtual para isolar as dependências
RUN uv venv /opt/venv

# --- INÍCIO DA CORREÇÃO ---
# Define a variável de ambiente para que 'uv' saiba onde instalar os pacotes.
# Isso "ativa" o venv para os próximos comandos RUN.
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# --- FIM DA CORREÇÃO ---

COPY pyproject.toml .

# Agora 'uv' (o global) instalará os pacotes corretamente dentro do VIRTUAL_ENV
RUN uv pip install --no-cache -r pyproject.toml


# =================================================================
# Estágio 2: "Final" - Configura o container de execução
# (Este estágio permanece o mesmo)
# =================================================================
FROM python:3.12-slim

WORKDIR /app

RUN adduser --system --no-create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY simple_streamable_http_mcp_server.py .

ENV PATH="/opt/venv/bin:$PATH"

USER appuser

EXPOSE 8000

CMD ["uvicorn", "simple_streamable_http_mcp_server:mcp", "--host", "0.0.0.0", "--port", "8000"]