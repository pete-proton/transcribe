#!/usr/bin/env python3
"""
Простой скрипт для транскрибации аудио
Использует faster-whisper (самый быстрый вариант)
"""

import argparse
import sys
from pathlib import Path
from faster_whisper import WhisperModel


def main():
    parser = argparse.ArgumentParser(
        description='Транскрибация аудио файлов с помощью Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s audio.opus
  %(prog)s audio.opus -l ru
  %(prog)s audio.opus -o result.txt
  %(prog)s audio.opus -m small -l ru -o transcription.txt

Размеры моделей:
  tiny   - ~75MB,  самая быстрая, менее точная
  base   - ~142MB, хороший баланс (по умолчанию)
  small  - ~461MB, хорошая точность для русского
  medium - ~1.5GB, высокая точность
  large  - ~2.9GB, максимальная точность
  turbo  - ~809MB, быстрая версия large-v3 (~8x быстрее)
        """
    )

    parser.add_argument(
        'input_file',
        type=str,
        help='Путь к аудио файлу для транскрибации'
    )

    parser.add_argument(
        '-l', '--language',
        type=str,
        default='ru',
        help='Язык аудио (по умолчанию: ru). Примеры: ru, en, es, de, fr'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Файл для сохранения результата (по умолчанию: <input_file>.txt)'
    )

    parser.add_argument(
        '-m', '--model',
        type=str,
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3', 'turbo'],
        help='Размер модели (по умолчанию: base)'
    )

    parser.add_argument(
        '--device',
        type=str,
        default='cpu',
        choices=['cpu', 'cuda'],
        help='Устройство для вычислений: cpu или cuda (по умолчанию: cpu)'
    )

    parser.add_argument(
        '--beam-size',
        type=int,
        default=5,
        help='Beam size для декодирования (по умолчанию: 5). Больше = точнее, но медленнее'
    )

    args = parser.parse_args()

    # Проверяем существование входного файла
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Ошибка: Файл не найден: {args.input_file}")
        sys.exit(1)

    # Определяем выходной файл
    if args.output:
        output_path = Path(args.output)
    else:
        # Заменяем расширение на .txt
        output_path = input_path.with_suffix('.txt')

    print("=" * 70)
    print(f"🎙️  Загрузка модели '{args.model}'...")
    print("   (При первом запуске модель будет скачана с HuggingFace)")
    print("=" * 70)

    # Создаём модель
    try:
        model = WhisperModel(
            args.model,
            device=args.device,
            compute_type="int8" if args.device == "cpu" else "float16"
        )
    except Exception as e:
        print(f"❌ Ошибка загрузки модели: {e}")
        sys.exit(1)

    print(f"\n📝 Транскрибация файла: {args.input_file}")
    print(f"🌍 Язык: {args.language}")
    print(f"🤖 Модель: {args.model}")
    print(f"💾 Выходной файл: {output_path}\n")

    # Транскрибируем
    try:
        segments, info = model.transcribe(
            str(input_path),
            language=args.language,
            beam_size=args.beam_size,
            vad_filter=True,  # Убирает тишину
        )

        # Выводим результаты
        print("=" * 70)
        print("РЕЗУЛЬТАТ:")
        print("=" * 70)

        full_text = []
        for segment in segments:
            text = segment.text.strip()
            timestamp = f"[{segment.start:.1f}s → {segment.end:.1f}s]"
            print(f"{timestamp:20s} {text}")
            full_text.append(text)

        print("\n" + "=" * 70)
        print("ВЕСЬ ТЕКСТ ЦЕЛИКОМ:")
        print("=" * 70)
        result = " ".join(full_text)
        print(result)

        # Сохраняем в файл
        output_path.write_text(result, encoding="utf-8")

        print(f"\n✅ Сохранено в файл: {output_path}")
        print(f"\n📊 Распознанный язык: {info.language} ({info.language_probability:.1%})")
        print(f"⏱️  Длительность аудио: {info.duration:.1f} секунд")

    except Exception as e:
        print(f"\n❌ Ошибка транскрибации: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()