# Настройка
```shell
. ./setup.sh
```

# Использование transcribe.py

## Базовое использование

### Только входной файл (язык: русский, выход: audio.txt)
```bash
python transcribe.py "WhatsApp Audio 2025-12-22 at 16.18.38.opus" -l es
```

### Входной файл + язык
```bash
python transcribe.py audio.opus -l ru
python transcribe.py audio.opus -l en
python transcribe.py audio.opus -l es
```

### Входной файл + выходной файл
```bash
python transcribe.py audio.opus -o result.txt
```

### Входной файл + язык + выходной файл
```bash
python transcribe.py audio.opus -l ru -o transcript.txt
python transcribe.py audio.opus -l en -o transcript.txt
python transcribe.py audio.opus -l es -o transcripcion.txt
```

## Примеры

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