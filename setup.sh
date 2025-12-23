#!/bin/bash
# install pyenv, see https://github.com/pyenv/pyenv
set -e

# Версия Python для установки
PYTHON_VERSION="3.12"

echo "Устанавливаем Python $PYTHON_VERSION через pyenv"
pyenv install $PYTHON_VERSION --skip-existing

echo "Устанавливаем версию Python $PYTHON_VERSION для проекта"
pyenv local $PYTHON_VERSION

echo "Создаём виртуальное окружение"
python -m venv myenv

echo "Активируем виртуальное окружение"
source myenv/bin/activate

echo "Устанавливаем зависимости"
pip install -r requirements.txt

brew install ffmpeg

echo "Установка завершена успешно!"