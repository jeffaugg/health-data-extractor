FROM python:3.9-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Configura diretório de trabalho
WORKDIR /app

# Copia arquivos necessários
COPY requirements.txt .
COPY src/ /app/src/
COPY Anexo.pdf .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Garante que o diretório de saída existe
RUN mkdir -p /app/output

CMD ["python", "src/script.py"]