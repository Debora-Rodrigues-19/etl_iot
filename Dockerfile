# Etapa base: imagem leve com Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY etl_iot.py /app/etl_iot.py

# Instala dependências
RUN pip install --no-cache-dir click requests mysql-connector-python

# Define o script como ponto de entrada
ENTRYPOINT ["python", "etl_iot.py"]
