# Используем официальный Python образ с версией 3.12-slim
FROM python:3.12-slim

# Отключаем запись pyc-файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в папку app
WORKDIR /app/app

# Устанавливаем системные зависимости (например, gcc)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь исходный код приложения в контейнер
COPY . /app

EXPOSE 7733

WORKDIR /app

# Запускаем приложение
CMD ["python", "app/main.py"]
