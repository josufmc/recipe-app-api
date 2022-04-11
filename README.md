# recipe-app-api
Recipe app source code

## Installation

Installation of Docker image

```bash
docker build .
```

Running from docker-compose

```bash
docker-compose build
```

## Start application

```bash
docker-compose up
```

## Run commands

It runs in the `WORKDIR` specified in Dockerfile

```bash
docker-compose run app sh -c "django-admin.py startproject app ."
```
