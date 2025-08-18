# Imagen base con Python 3.11 (puedes usar 3.10 si prefieres)
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt y app.py al contenedor
COPY requirements.txt .
COPY app.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde correrá Flask
EXPOSE 8080

# Variable de entorno (opcional, se puede pasar al correr)
# ENV ABUSEIPDB_API_KEY=tu_api_key

# Comando para ejecutar la API
CMD ["python", "app.py"]
