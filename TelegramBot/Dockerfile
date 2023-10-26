# Usa la imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo
WORKDIR /app

# Copia tu código al contenedor
COPY . /app

# Instala las dependencias
RUN pip install -r requirements.txt

# Ejecuta tu aplicación
CMD ["python", "bot.py"]