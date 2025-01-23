<div align="center">
<h1>Менеджер задач / Task manager</h1>
</div>

<div align="center">

[![Actions Status](https://github.com/zainutdinov/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/zainutdinov/python-project-52/actions) [![Maintainability](https://api.codeclimate.com/v1/badges/716ca67008ef14b45bf1/maintainability)](https://codeclimate.com/github/zainutdinov/python-project-52/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/716ca67008ef14b45bf1/test_coverage)](https://codeclimate.com/github/zainutdinov/python-project-52/test_coverage) [![Python CI](https://github.com/zainutdinov/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/zainutdinov/python-project-52/actions/workflows/pyci.yml)

</div>

### Render
https://task-manager-tst7.onrender.com


## Описание проекта

**«Task Manager»** – система управления задачами. Она позволяет ставить задачи, назначать исполнителей и менять их статусы. Для работы с системой требуется регистрация и аутентификация.

## Требования

- Python ^3.11.11
- django ^5.1.4
- PostgreSQL

## Инструкция по установке

> Чтобы использовать пакет, вам нужно скопировать репозиторий на свой компьютер. Это делается с помощью команды ``git clone``:

```bash
git clone https://github.com/zainutdinov/python-project-52
```

> Создайте файл .env в корневой директории проекта. Добавьте в него две переменные: DATABASE_URL и SECRET_KEY.

- SECRET_KEY может быть сгенерирован или введён вручную (Django secret key)
- DATABASE_URL должен иметь следующий формат: {provider}://{user}:{password}@{host}:{port}/{db (DATABASE_URL не обязательна, если используете SQLite)

> Сделайте скрипт build.sh исполняемым:

- Перейдите в директорию проекта
```bash
cd python-project-52
```

- Далее сделайте скрипт исполняемым
```bash
chmod +x ./build.sh
```

> Выполните установку пакета и настройте базу данных:

```bash
make build
```

> Для запуска в dev mode используйте команду:
```bash
make dev
```
URL-адрес сервера: http://127.0.0.1:8000.

#### При деплое на PaaS установите переменные ACCESS_TOKEN, DATABASE_URL, SECRET_KEY

- В настройках сервиса установите команды

Build Command:
```bash
make build
```

Start Command
```bash
make start
```

## Линтер и тесты

- Для проверки линтером ruff:
```bash
make lint
```

- Для исправления линтером ruff ошибок:
```bash
make lint-fix
```

- Для запуска тестов:
```bash
make test
```

- Покрытие кода тестами:
```bash
make test-coverage
```