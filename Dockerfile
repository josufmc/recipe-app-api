FROM python:3.7-alpine

# Recomendado, no permite a Python almacenar en búffer las salidas
# lo imprime directamente. Evita complicaciones
ENV PYTHONUNBUFFERED 1  

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
# Las aplicaciones correrán desde esta ubicación por defecto
WORKDIR /app
COPY ./app /app

# Create user for running apps only (Only processes, not shell)
# For security purposes. If not, it will use root
RUN adduser -D user
USER user
