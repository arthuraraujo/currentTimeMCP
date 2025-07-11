# Dockerfile

# Passo 1: Usar uma imagem base oficial do Python com Alpine Linux
# É uma imagem leve, ideal para produção.
FROM python:3.11-alpine

# Passo 2: Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Passo 3: Copiar o arquivo de dependências para o diretório de trabalho
# Copiamos este arquivo primeiro para aproveitar o cache do Docker.
COPY requirements.txt .

# Passo 4: Instalar as dependências
# O --no-cache-dir garante que o cache do pip não seja armazenado, mantendo a imagem menor.
RUN pip install --no-cache-dir -r requirements.txt

# Passo 5: Copiar todo o código da aplicação para o diretório de trabalho
COPY . .

# Passo 6: Expor a porta em que a aplicação irá rodar
EXPOSE 5000

# Passo 7: Comando para iniciar a aplicação em produção usando Gunicorn
# "app:app" refere-se ao arquivo app.py e à instância "app" do Flask dentro dele.
# --bind 0.0.0.0:5000 faz o servidor escutar em todas as interfaces de rede.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]