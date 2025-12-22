#!/usr/bin/env python3
"""
Простой скрипт для транскрибации аудио
Использует faster-whisper (самый быстрый вариант)
"""

from faster_whisper import WhisperModel

# Путь к вашему аудио файлу
AUDIO_FILE = "WhatsApp Audio 2025-12-22 at 16.18.38.opus"

# Выберите размер модели:
# "tiny"   - ~75MB, самая быстрая, менее точная
# "base"   - ~142MB, хороший баланс скорости и точности  ⭐ РЕКОМЕНДУЕТСЯ
# "small"  - ~461MB, хорошая точность для русского
# "medium" - ~1.5GB, высокая точность
# "large"  - ~2.9GB, максимальная точность
MODEL_SIZE = "base"

# Язык аудио
# LANGUAGE = "ru"
LANGUAGE = "es"

print(f"🎙️  Загрузка модели '{MODEL_SIZE}'...")
print("   (При первом запуске модель будет скачана с HuggingFace)")

# Создаём модель
# device="cuda" - для Nvidia GPU (намного быстрее)
# device="cpu"  - для процессора
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

print(f"\n📝 Транскрибация файла: {AUDIO_FILE}\n")

# Транскрибируем
segments, info = model.transcribe(
    AUDIO_FILE,
    language=LANGUAGE,
    beam_size=5,  # Чем больше - тем точнее, но медленнее
    vad_filter=True,  # Убирает тишину
)

# Выводим результаты
print("="*70)
print("РЕЗУЛЬТАТ:")
print("="*70)

full_text = []
for segment in segments:
    text = segment.text.strip()
    timestamp = f"[{segment.start:.1f}s → {segment.end:.1f}s]"
    print(f"{timestamp:20s} {text}")
    full_text.append(text)

print("\n" + "="*70)
print("ВЕСЬ ТЕКСТ ЦЕЛИКОМ:")
print("="*70)
result = " ".join(full_text)
print(result)

# Сохраняем в файл
output_file = AUDIO_FILE.replace(".opus", ".txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(result)

print(f"\n✅ Сохранено в файл: {output_file}")
print(f"\n📊 Распознанный язык: {info.language} ({info.language_probability:.1%})")
print(f"⏱️  Длительность аудио: {info.duration:.1f} секунд")