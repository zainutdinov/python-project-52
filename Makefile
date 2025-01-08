install:
	uv sync

build:
	./build.sh

start:
	python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
