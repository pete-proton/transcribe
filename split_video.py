#!/usr/bin/env python3
"""
Video file splitter - splits large files into chunks of specified size.
"""

import os
import sys
from pathlib import Path


def split_file(input_file: str, max_chunk_size_gb: float = 4.0):
    """
    Split a file into chunks of specified maximum size.

    Args:
        input_file: Path to the input file
        max_chunk_size_gb: Maximum size of each chunk in GB (default: 4.0)
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)

    # Calculate chunk size in bytes
    chunk_size = int(max_chunk_size_gb * 1024 * 1024 * 1024)

    # Get file size
    file_size = input_path.stat().st_size
    file_size_gb = file_size / (1024 ** 3)

    print(f"Input file: {input_path.name}")
    print(f"File size: {file_size_gb:.2f} GB")
    print(f"Chunk size: {max_chunk_size_gb} GB")

    # Calculate number of chunks needed
    num_chunks = (file_size + chunk_size - 1) // chunk_size
    print(f"Will create {num_chunks} chunk(s)")

    # Get output file pattern (same name with .part01, .part02, etc.)
    base_name = input_path.stem
    extension = input_path.suffix
    output_dir = input_path.parent

    # Split the file
    chunk_num = 1
    bytes_read = 0

    with open(input_path, 'rb') as input_file_obj:
        while True:
            # Read chunk
            chunk_data = input_file_obj.read(chunk_size)
            if not chunk_data:
                break

            # Create output filename with zero-padded number
            output_filename = f"{base_name}.part{chunk_num:02d}{extension}"
            output_path = output_dir / output_filename

            # Write chunk
            print(f"Writing {output_filename}...", end=' ')
            with open(output_path, 'wb') as output_file:
                output_file.write(chunk_data)

            chunk_size_written = len(chunk_data)
            bytes_read += chunk_size_written
            print(f"({chunk_size_written / (1024 ** 3):.2f} GB)")

            chunk_num += 1

    print(f"\nDone! Created {chunk_num - 1} chunk(s)")
    print(f"Total bytes processed: {bytes_read / (1024 ** 3):.2f} GB")

    # Print reassembly command
    print(f"\nTo reassemble the file, use:")
    print(f"  cat {base_name}.part*{extension} > {input_path.name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python split_video.py <input_file> [max_size_gb]")
        print("Example: python split_video.py video.mov 4")
        sys.exit(1)

    input_file = sys.argv[1]
    max_size_gb = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0

    split_file(input_file, max_size_gb)


if __name__ == "__main__":
    main()