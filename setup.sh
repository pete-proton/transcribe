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

# ========================================================================
# ffmpeg-full - нужно ИМЕННО full, не regular ffmpeg!
# ------------------------------------------------------------------------
# Regular `ffmpeg` не имеет libass / libfreetype / drawtext filter,
# поэтому НЕ может burn субтитры на видео.
#
# `ffmpeg-full` включает:
#   - libass         (subtitles filter - render SRT/ASS)
#   - libfreetype    (drawtext filter)
#   - libfontconfig  (font lookup)
#   - libtesseract   (OCR из видео)
#   - libwhisper     (transcription прямо в ffmpeg pipeline)
#   - libplacebo, harfbuzz, и др. (~46 deps)
#
# Если уже установлен regular ffmpeg - снести:
#   brew uninstall ffmpeg
#
# `ffmpeg-full` это keg-only formula. После установки бинарь
# доступен по полному пути:
#   /opt/homebrew/Cellar/ffmpeg-full/<version>/bin/ffmpeg
#
# Чтобы команда `ffmpeg` использовала full - force-link:
#   brew link ffmpeg-full --force
# ========================================================================
brew install ffmpeg-full
brew link ffmpeg-full --force --overwrite

# ========================================================================
# whisper-cpp - C++ Whisper для генерации SRT с timestamps
# ------------------------------------------------------------------------
# faster-whisper (Python) тоже умеет генерить SRT, но whisper-cpp
# работает заметно быстрее на Apple Silicon через Metal/CoreML.
#
# Подробнее по моделям в README.md.
# Скачать модель отдельно:
#   bash <(curl -s https://raw.githubusercontent.com/ggml-org/whisper.cpp/master/models/download-ggml-model.sh) large-v3-turbo
# Положить в ~/.cache/whisper-models/
# ========================================================================
brew install whisper-cpp

# Скачать модель large-v3-turbo (Mac-optimized, ~800MB)
# если ещё нет
MODELS_DIR="$HOME/.cache/whisper-models"
mkdir -p "$MODELS_DIR"
if [ ! -f "$MODELS_DIR/ggml-large-v3-turbo.bin" ]; then
  echo "Скачиваем модель large-v3-turbo..."
  curl -L -o "$MODELS_DIR/ggml-large-v3-turbo.bin" \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"
fi

echo "Установка завершена успешно!"
echo
echo "Проверка:"
echo "  ffmpeg -filters | grep -E 'subtitles|drawtext|ass '"
echo "  whisper-cli --help"
