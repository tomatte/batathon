FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /app

COPY . .

RUN uv sync --locked

RUN uv run playwright install

EXPOSE 8001

CMD ["uv", "run", "fastapi", "dev", "./src/chatbot/main.py", "--host", "0.0.0.0", "--port", "8000"]
