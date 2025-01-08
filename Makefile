install:
	uv sync

build:
	./build.sh

start:
	uv run python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker
