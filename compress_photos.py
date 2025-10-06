#!/usr/bin/env python3
"""
Compress photos to reduce file size for web use.
This will compress images to ~80% quality and max 1920px width.
"""

from PIL import Image
import os
import sys

def compress_image(input_path, output_path, max_width=1920, quality=80):
    """Compress an image while maintaining aspect ratio."""
    try:
        img = Image.open(input_path)

        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Resize if wider than max_width
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # Save with compression
        img.save(output_path, 'JPEG', quality=quality, optimize=True)

        # Get file sizes
        original_size = os.path.getsize(input_path) / 1024 / 1024  # MB
        compressed_size = os.path.getsize(output_path) / 1024 / 1024  # MB
        reduction = ((original_size - compressed_size) / original_size) * 100

        print(f"✓ {os.path.basename(input_path)}: {original_size:.2f}MB → {compressed_size:.2f}MB ({reduction:.1f}% reduction)")
        return True

    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")
        return False

def compress_directory(directory):
    """Compress all images in a directory."""
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    print(f"\nCompressing images in: {directory}")
    print("-" * 60)

    compressed_count = 0
    total_original = 0
    total_compressed = 0

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(directory, filename)

            # Create output filename (change to .jpg if .png)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(directory, f"{base_name}_compressed.jpg")

            original_size = os.path.getsize(input_path) / 1024 / 1024

            if compress_image(input_path, output_path):
                compressed_size = os.path.getsize(output_path) / 1024 / 1024
                total_original += original_size
                total_compressed += compressed_size
                compressed_count += 1

    if compressed_count > 0:
        total_reduction = ((total_original - total_compressed) / total_original) * 100
        print("-" * 60)
        print(f"Compressed {compressed_count} images")
        print(f"Total: {total_original:.2f}MB → {total_compressed:.2f}MB ({total_reduction:.1f}% reduction)")
        print(f"\nCompressed files saved with '_compressed.jpg' suffix.")
        print(f"Review them, then delete originals and rename compressed versions.")

if __name__ == "__main__":
    print("=" * 60)
    print("Wedding Photo Compression Tool")
    print("=" * 60)

    party_dir = "wedding/static/wedding/images/party"
    locations_dir = "wedding/static/wedding/images/locations"

    if os.path.exists(party_dir):
        compress_directory(party_dir)

    if os.path.exists(locations_dir):
        compress_directory(locations_dir)

    print("\n" + "=" * 60)
    print("Done! Upload compressed images to Google Drive to save space.")
    print("=" * 60)
