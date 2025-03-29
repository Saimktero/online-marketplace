#!/bin/bash

echo "📁 Создаём папку staticfiles (если нет)..."
mkdir -p staticfiles

echo "📦 Собираем статику..."
python3 manage.py collectstatic --noinput
