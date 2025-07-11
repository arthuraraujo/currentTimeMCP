# =================================================================
# Estágio 1: "Builder" - Instala dependências
# Usamos uma imagem slim do Python para manter o tamanho reduzido.
# =================================================================
FROM python:3.12-slim as builder

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o 'uv', um instalador de pacotes Python rápido, como recomendado
RUN pip install uv

# Cria um ambiente virtual para isolar as dependências da aplicação
RUN uv venv /opt/venv

# Copia o arquivo de dependências para o container
# Fazemos isso em um passo separado para aproveitar o cache do Docker.
# A reinstalação das dependências só ocorrerá se este arquivo mudar.
COPY pyproject.toml .

# Instala as dependências do projeto no ambiente virtual usando 'uv'
# A flag --no-cache ajuda a manter o tamanho da camada do Docker menor
RUN /opt/venv/bin/uv pip install --no-cache -r pyproject.toml


# =================================================================
# Estágio 2: "Final" - Configura o container de execução
# Partimos da mesma imagem base limpa para criar o container final.
# =================================================================
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Cria um usuário e grupo 'appuser' sem privilégios de root para segurança
RUN adduser --system --no-create-home appuser

# Copia o ambiente virtual com as dependências já instaladas do estágio "builder"
COPY --from=builder /opt/venv /opt/venv

# Copia o código da sua aplicação para o container
COPY simple_streamable_http_mcp_server.py .

# Adiciona o diretório 'bin' do ambiente virtual ao PATH do sistema
# Isso permite executar comandos como 'uvicorn' diretamente.
ENV PATH="/opt/venv/bin:$PATH"

# Troca para o usuário sem privilégios que criamos
USER appuser

# Expõe a porta 8000, que é a porta padrão onde o Uvicorn irá rodar
EXPOSE 8000

# Define o comando para iniciar a aplicação quando o container for executado
# Executamos 'uvicorn' diretamente para ter controle sobre o host e a porta.
# O host '0.0.0.0' é essencial para que o servidor seja acessível de fora do container.
# 'simple_streamable_http_mcp_server:mcp' aponta para a instância ASGI 'mcp' no seu arquivo.
CMD ["uvicorn", "simple_streamable_http_mcp_server:mcp", "--host", "0.0.0.0", "--port", "5000"]