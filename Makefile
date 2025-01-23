install:
	uv sync

build:
	./build.sh

start:
	python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

migrate:
	uv run python manage.py makemigrations && \
	uv run python manage.py migrate

test:
	uv run python manage.py test

test-coverage:
	DJANGO_SETTINGS_MODULE=task_manager.settings uv run pytest --cov=task_manager --cov-report=xml

make dev:
	uv run python manage.py runserver