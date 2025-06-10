fastapi:
	fastapi dev ./src/chatbot/main.py

all: fastapi

install:
	uv pip install -r pyproject.toml

activate:
	source ./.venv/bin/activate

venv:
	uv venv

start:
	uv run ./src/chatbot/main.py

cli:
	uv run ./src/chatbot/cli.py

mcp:
	uv run ./src/mcp_server/server.py