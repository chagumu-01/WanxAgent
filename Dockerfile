FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/backend /app/src/backend

WORKDIR /app/src/backend

EXPOSE 7860

CMD ["uvicorn", "agentchat.main:app", "--host", "0.0.0.0", "--port", "7860"]