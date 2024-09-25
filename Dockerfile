# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de la aplicación
COPY . /app

# Crea un entorno virtual
RUN python -m venv /opt/venv

# Activa el entorno virtual y instala las dependencias de Python
RUN . /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Establece las variables de entorno para el entorno virtual
ENV PATH="/opt/venv/bin:$PATH"

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]