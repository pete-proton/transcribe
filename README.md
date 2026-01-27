# Настройка
```bash
. ./setup.sh
```

# Использование transcribe.py

## Базовое использование

### Аудио файлы (OPUS, MP3, WAV и т.д.)
```bash
python transcribe.py "WhatsApp Audio 2025-12-23 at 10.28.15.opus" -l ru -m large-v3
```

### Видео файлы (MOV, MP4, AVI и т.д.)
Скрипт автоматически извлечёт аудио дорожку из видео:
```bash
python transcribe.py "Screen Recording 2025-12-23 at 13.32.57.mov" -l ru -m large-v3
```

### Входной файл + язык
```bash
python transcribe.py audio.opus -l ru
python transcribe.py video.mov -l en
python transcribe.py audio.opus -l es
```

### Входной файл + выходной файл
```bash
python transcribe.py audio.opus -o result.txt
python transcribe.py video.mov -o transcript.txt
```

### Входной файл + язык + выходной файл
```bash
python transcribe.py audio.opus -l ru -o transcript.txt
python transcribe.py video.mov -l en -o transcript.txt
python transcribe.py audio.opus -l es -o transcripcion.txt
python transcribe.py "Screen Recording 2025-12-23 at 13.32.57.mov" -l en -m large-v3
```

## Примеры

### Аудио файлы
```bash
# Русское аудио → audio.txt
python transcribe.py audio.opus

# Английское аудио → audio.txt
python transcribe.py audio.opus -l en

# Русское аудио → мой_файл.txt
python transcribe.py audio.opus -o мой_файл.txt

# Испанское аудио → resultado.txt
python transcribe.py audio.opus -l es -o resultado.txt
```

### Видео файлы
```bash
# Видео запись экрана → transcript.txt (русский)
python transcribe.py "Screen Recording 2025-12-23 at 13.32.57.mov" -l ru

# Видео на английском → english_transcript.txt
python transcribe.py video.mov -l en -o english_transcript.txt

# С моделью small (быстрее, но менее точно)
python transcribe.py video.mov -l ru -m small

# С моделью large-v3 (медленнее, но максимальная точность)
python transcribe.py "WhatsApp Audio 2026-01-27 at 10.14.35.opus" -l ru -m large-v3
```

## Размеры моделей
- `tiny` - ~75MB, самая быстрая, менее точная
- `base` - ~142MB, хороший баланс (по умолчанию)
- `small` - ~461MB, хорошая точность для русского
- `medium` - ~1.5GB, высокая точность
- `large-v3` - ~2.9GB, максимальная точность (рекомендуется для русского)

## Коды языков
- `ru` - русский
- `en` - английский
- `es` - испанский
- `de` - немецкий
- `fr` - французский
- `it` - итальянский
- `pt` - португальский
- `zh` - китайский
- `ja` - японский

# Использование split_video

Разделение больших видео файлов на части заданного размера:

```bash
# С размером по умолчанию (4 GB)
python split_video.py "Screen Recording 2025-12-23 at 13.32.57.mov"

# С размером 3.9 GB
python split_video.py "Screen Recording 2025-12-23 at 13.32.57.mov" 3.9

# С размером 2 GB
python split_video.py "Screen Recording 2025-12-23 at 13.32.57.mov" 2

# Результат: файлы вида
# Screen Recording 2025-12-23 at 13.32.57.part01.mov
# Screen Recording 2025-12-23 at 13.32.57.part02.mov
# и т.д.
```

## Сборка разделённых файлов обратно
```bash
# macOS/Linux
cat "Screen Recording 2025-12-23 at 13.32.57.part"*.mov > "Screen Recording 2025-12-23 at 13.32.57.mov"

# Windows (PowerShell)
Get-Content "Screen Recording 2025-12-23 at 13.32.57.part*.mov" -Raw | Set-Content "Screen Recording 2025-12-23 at 13.32.57.mov"
```

# Типичный workflow для больших видео

1. **Разделить большой MOV файл на части:**
   ```bash
   python split_video.py "recording.mov" 3.9
   ```

2. **Транскрибировать каждую часть:**
   ```bash
   python transcribe.py "recording.part01.mov" -l ru -m large-v3 -o part01.txt
   python transcribe.py "recording.part02.mov" -l ru -m large-v3 -o part02.txt
   python transcribe.py "recording.part03.mov" -l ru -m large-v3 -o part03.txt
   ```

3. **Объединить результаты:**
   ```bash
   cat part01.txt part02.txt part03.txt > full_transcript.txt
   ```