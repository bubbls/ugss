#!/usr/bin/env python3
"""
Split large files into 19MB chunks.
Scans a folder for files over 20MB and splits them into .part1, .part2, etc.
"""

import os
import sys
import math
import argparse

MB = 1024 * 1024
SIZE_THRESHOLD = 20 * MB   # Files larger than this will be split
CHUNK_SIZE     = 19 * MB   # Each chunk will be this size


def split_file(filepath: str) -> None:
    """Split a single file into 19MB chunks."""
    file_size = os.path.getsize(filepath)
    total_parts = math.ceil(file_size / CHUNK_SIZE)
    padding = len(str(total_parts))

    print(f"  Splitting: {os.path.basename(filepath)}")
    print(f"    Size   : {file_size / MB:.2f} MB")
    print(f"    Parts  : {total_parts}")

    with open(filepath, "rb") as src:
        for part_num in range(1, total_parts + 1):
            chunk = src.read(CHUNK_SIZE)
            if not chunk:
                break

            part_filename = f"{filepath}.part{str(part_num).zfill(padding)}"
            with open(part_filename, "wb") as dst:
                dst.write(chunk)

            part_size = len(chunk) / MB
            print(f"    Created: {os.path.basename(part_filename)} ({part_size:.2f} MB)")

    print(f"  Done — {total_parts} part(s) created.\n")


def scan_and_split(folder: str, delete_original: bool = False) -> None:
    """Scan a folder for files over 20MB and split them."""
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning folder: {os.path.abspath(folder)}")
    print(f"Threshold : {SIZE_THRESHOLD / MB:.0f} MB")
    print(f"Chunk size: {CHUNK_SIZE / MB:.0f} MB\n")

    found = False
    for dirpath, dirnames, filenames in os.walk(folder):
        dirnames.sort()  # Walk subdirectories in alphabetical order
        for filename in sorted(filenames):
            # Skip already-split parts
            if ".part" in filename and filename.rsplit(".part", 1)[-1].isdigit():
                continue

            filepath = os.path.join(dirpath, filename)
            if os.path.getsize(filepath) > SIZE_THRESHOLD:
                found = True
                split_file(filepath)

                if delete_original:
                    os.remove(filepath)
                    print(f"  Deleted original: {filename}\n")

    if not found:
        print("No files over 20 MB found.")


def main():
    parser = argparse.ArgumentParser(
        description="Split files over 20 MB into 19 MB chunks."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder to scan (default: current directory)"
    )
    parser.add_argument(
        "--delete-original",
        action="store_true",
        help="Delete the original file after splitting"
    )
    args = parser.parse_args()

    scan_and_split(args.folder, delete_original=args.delete_original)


if __name__ == "__main__":
    main()