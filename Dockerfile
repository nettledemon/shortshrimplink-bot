# базовый образ
FROM python:3.14-slim

# рабочая директория внутри контейнера
WORKDIR /app

# файл с зависимостями
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# команда по умолчанию (будет docker-compose)
CMD ["python", "src/main.py"]