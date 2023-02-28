# README

This README would normally document whatever steps are necessary to get your application up and running.

- First steps

### Create venv

python3 -m venv venv

### Run venv

source venv/bin/activate

### Install Fast API

pip install fastapi

### or

pip3 install fastapi

### Install Uvicorn

pip install "uvicorn[standard]"

### or

pip3 install "uvicorn[standard]"

### Run this application

uvicorn app.main:app --reload

### Add dependencies to requirements.txt

pip3 freeze > requirements.txt

### or

pip freeze > requirements.txt

### Install dependencies

pip3 install -r requirements.txt

# RUN local

docker-compose up --build

# BUILD

sudo docker-compose -f docker-compose.prod.yml up --build -d

# UP

sudo docker-compose -f docker-compose.prod.yml up -d

# Containers

## List containers

docker ps

## Enter a container

docker exec -it <id> bash

## Running migrations

Running new migration

```bash
alembic revision --autogenerate -m "Migration name"
```

Undo last migration

```bash
alembic downgrade -1
```

Updating migrations

```bash
alembic upgrade head
```
