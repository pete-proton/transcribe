# Настройка
```bash
. ./setup.sh
```

# Использование

```bash
python transcribe.py "Swiftly-TTD tech call.m4a" -l en -m turbo
python transcribe.py video.mov -l en -o result.txt
```

## Размеры моделей
- `tiny` - ~75MB, самая быстрая, менее точная
- `base` - ~142MB, хороший баланс (по умолчанию)
- `small` - ~461MB, хорошая точность для русского
- `medium` - ~1.5GB, высокая точность
- `large-v3` - ~2.9GB, максимальная точность
- `turbo` - ~809MB, быстрая версия large-v3 (~8x быстрее)

## Коды языков
`ru` русский, `en` английский, `es` испанский, `de` немецкий, `fr` французский, `zh` китайский, `ja` японский

# Разделение больших видео

```bash
# Разделить на части по 3.9 GB
python split_video.py "recording.mov" 3.9

# Транскрибировать каждую часть
python transcribe.py "recording.part01.mov" -l ru -m turbo -o part01.txt
python transcribe.py "recording.part02.mov" -l ru -m turbo -o part02.txt

# Объединить результаты
cat part01.txt part02.txt > full_transcript.txt
```
