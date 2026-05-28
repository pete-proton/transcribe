#!/usr/bin/env python3
"""Translate SRT file from one language to another using Google Translate via deep-translator."""

import sys
import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator


def parse_srt(content):
    """Parse SRT content into list of (idx, timestamp, text) tuples."""
    blocks = re.split(r'\n\s*\n', content.strip())
    parsed = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        idx = lines[0].strip()
        timestamp = lines[1].strip()
        text = '\n'.join(lines[2:]).strip()
        parsed.append((idx, timestamp, text))
    return parsed


def write_srt(segments, output_path):
    """Write segments back to SRT format."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, timestamp, text in segments:
            f.write(f"{idx}\n{timestamp}\n{text}\n\n")


def translate_batch(texts, src='es', dst='ru', batch_size=50):
    """Translate texts in batches with progress."""
    translator = GoogleTranslator(source=src, target=dst)
    results = []
    total = len(texts)
    for i in range(0, total, batch_size):
        batch = texts[i:i+batch_size]
        # deep-translator supports batch translation
        try:
            translated = translator.translate_batch(batch)
        except Exception as e:
            print(f"  Batch {i}-{i+len(batch)} failed: {e}, retrying per-segment...", file=sys.stderr)
            translated = []
            for t in batch:
                try:
                    translated.append(translator.translate(t))
                except Exception as e2:
                    print(f"    Item failed: {e2}", file=sys.stderr)
                    translated.append(t)  # fallback: original
                time.sleep(0.1)
        results.extend(translated)
        done = min(i+batch_size, total)
        print(f"  [{done}/{total}] {int(done/total*100)}%", flush=True)
        time.sleep(0.5)  # rate limit politeness
    return results


def main():
    if len(sys.argv) != 4:
        print("Usage: translate_srt.py <input.srt> <output.srt> <src,dst>", file=sys.stderr)
        print("  e.g. translate_srt.py a.srt a-ru.srt es,ru", file=sys.stderr)
        sys.exit(1)

    inp, outp, langs = sys.argv[1], sys.argv[2], sys.argv[3]
    src, dst = langs.split(',')

    content = Path(inp).read_text(encoding='utf-8')
    segments = parse_srt(content)
    print(f"Parsed {len(segments)} segments from {inp}", flush=True)

    texts = [s[2] for s in segments]
    print(f"Translating {src} -> {dst}...", flush=True)
    translated = translate_batch(texts, src=src, dst=dst, batch_size=50)

    new_segments = [(s[0], s[1], t or s[2]) for s, t in zip(segments, translated)]
    write_srt(new_segments, outp)
    print(f"Wrote {outp}", flush=True)


if __name__ == '__main__':
    main()
