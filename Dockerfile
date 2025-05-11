FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала копируем только requirements.txt для кэширования
COPY requirements.txt .

# Установка зависимостей с очисткой кэша
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]