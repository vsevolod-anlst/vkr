FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

ENV PIP_DEFAULT_TIMEOUT=300

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "app.api"]
