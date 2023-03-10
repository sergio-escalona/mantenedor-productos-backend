# README

This README would normally document whatever steps are necessary to get your application up and running.

- First steps

# BUILD

docker-compose up --build

# UP

docker-compose up
### Add dependencies to requirements.txt

pip3 freeze > requirements.txt

### or

pip freeze > requirements.txt

### Install dependencies

pip3 install -r requirements.txt

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
