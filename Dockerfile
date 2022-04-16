FROM python:3.7-alpine

# Recomendado, no permite a Python almacenar en búffer las salidas
# lo imprime directamente. Evita complicaciones
ENV PYTHONUNBUFFERED 1  

COPY ./requirements.txt /requirements.txt
# Postgres dependencies (--no-cache es buena práctica para no añadir archivos extra)
RUN apk add --update --no-cache postgresql-client
# Creamos una instalación de dependencias virtuales para la instalación del cliente Postgres en Python
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
# Ya no lo noecesitamos por que lo podemos borrar esas dependencias virtuales
RUN apk del .tmp-build-deps

RUN mkdir /app
# Las aplicaciones correrán desde esta ubicación por defecto
WORKDIR /app
COPY ./app /app

# Create user for running apps only (Only processes, not shell)
# For security purposes. If not, it will use root
RUN adduser -D user
USER user
