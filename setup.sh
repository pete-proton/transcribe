#!/bin/bash
# Можно запускать как `./setup.sh` или `. ./setup.sh` (тогда venv останется активным).
# Вся установка идёт в subshell с `set -e`, чтобы при ошибке не закрывался
# текущий терминал, если скрипт был запущен через `.`.

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

(
set -e
cd "$PROJECT_DIR"

# Версия Python для установки
PYTHON_VERSION="3.12"

# Python 3.12 берём из Homebrew (pyenv не нужен).
# Если pyenv всё же установлен - используем его.
if command -v pyenv >/dev/null 2>&1; then
  echo "Устанавливаем Python $PYTHON_VERSION через pyenv"
  pyenv install "$PYTHON_VERSION" --skip-existing
  pyenv local "$PYTHON_VERSION"
  PYTHON="$(pyenv which python)"
else
  echo "Устанавливаем Python $PYTHON_VERSION через Homebrew"
  brew list --versions "python@$PYTHON_VERSION" >/dev/null || brew install "python@$PYTHON_VERSION"
  PYTHON="$(brew --prefix "python@$PYTHON_VERSION")/bin/python$PYTHON_VERSION"
fi

if [ ! -x myenv/bin/python ]; then
  echo "Создаём виртуальное окружение"
  "$PYTHON" -m venv myenv
fi

echo "Устанавливаем зависимости"
myenv/bin/python -m pip install --upgrade pip
myenv/bin/python -m pip install -r requirements.txt

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
brew install whisper.cpp

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
)
SETUP_STATUS=$?

if [ $SETUP_STATUS -ne 0 ]; then
  echo "Установка прервалась с ошибкой ($SETUP_STATUS)" >&2
  return $SETUP_STATUS 2>/dev/null || exit $SETUP_STATUS
fi

# Активация имеет смысл только при запуске через `. ./setup.sh`
if (return 0 2>/dev/null); then
  source "$PROJECT_DIR/myenv/bin/activate"
  echo "Виртуальное окружение myenv активировано"
else
  echo
  echo "Активировать окружение: source myenv/bin/activate"
fi
