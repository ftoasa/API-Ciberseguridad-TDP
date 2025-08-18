# Imagen base ligera de Python
   FROM python:3.10-slim

   # Directorio de trabajo
   WORKDIR /app

   # Copia el código y requirements
   COPY app.py requirements.txt /app/

   # Instala dependencias
   RUN pip install -r requirements.txt

   # Expone el puerto
   EXPOSE 8080

   # Comando para correr la app
   CMD ["python", "app.py"]