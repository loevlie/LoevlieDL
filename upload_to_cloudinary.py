#!/usr/bin/env python3
"""
Upload wedding photos to Cloudinary.
This will upload all photos from your local directories to Cloudinary.
Large files are automatically compressed to fit under the 10MB limit.
"""

import cloudinary
import cloudinary.uploader
import os
from pathlib import Path
from PIL import Image
import tempfile

# Configure Cloudinary
cloudinary.config(
    cloud_name="dbfcmocxi",
    api_key="551599118729589",
    api_secret="0qjREOdUh1bqt-jxBrWQ3_WecDY",
    secure=True
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

def compress_image_if_needed(file_path):
    """Compress image if it's over 10MB. Returns path to use for upload."""
    file_size = os.path.getsize(file_path)

    if file_size <= MAX_FILE_SIZE:
        return file_path, False  # No compression needed

    # Need to compress
    print(f"   📦 Compressing ({file_size / 1024 / 1024:.1f}MB -> ", end="")

    try:
        img = Image.open(file_path)

        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_path = temp_file.name
        temp_file.close()

        # Try different quality levels until under 10MB
        # Start at 95 for best quality, reduce by smaller increments
        quality = 95
        while quality > 60:
            img.save(temp_path, 'JPEG', quality=quality, optimize=True)
            compressed_size = os.path.getsize(temp_path)

            if compressed_size <= MAX_FILE_SIZE:
                print(f"{compressed_size / 1024 / 1024:.1f}MB, quality={quality})...", end=" ")
                return temp_path, True  # Return compressed file

            quality -= 2  # Smaller steps for finer control

        # If still too large, resize slightly and try again
        max_dimension = 3200  # Higher resolution before resizing
        if img.width > max_dimension or img.height > max_dimension:
            if img.width > img.height:
                new_width = max_dimension
                new_height = int(img.height * (max_dimension / img.width))
            else:
                new_height = max_dimension
                new_width = int(img.width * (max_dimension / img.height))

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img.save(temp_path, 'JPEG', quality=92, optimize=True)
            compressed_size = os.path.getsize(temp_path)
            print(f"{compressed_size / 1024 / 1024:.1f}MB, resized to {new_width}x{new_height})...", end=" ")
            return temp_path, True

        return temp_path, True

    except Exception as e:
        print(f"Compression failed: {e}")
        return file_path, False

def upload_directory(local_dir, cloudinary_folder):
    """Upload all images from local directory to Cloudinary folder."""
    if not os.path.exists(local_dir):
        print(f"❌ Directory not found: {local_dir}")
        return

    print(f"\n{'='*60}")
    print(f"📁 Local: {local_dir}")
    print(f"☁️  Cloudinary: {cloudinary_folder}")
    print(f"{'='*60}\n")

    uploaded = 0
    failed = 0
    compressed_count = 0

    for filename in os.listdir(local_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(local_dir, filename)

            try:
                print(f"⬆️  Uploading: {filename}...", end=" ")

                # Compress if needed
                upload_path, was_compressed = compress_image_if_needed(file_path)
                if was_compressed:
                    compressed_count += 1

                result = cloudinary.uploader.upload(
                    upload_path,
                    folder=cloudinary_folder,
                    resource_type="image",
                    overwrite=True,
                    transformation=[
                        {'quality': 'auto:good'},  # Auto optimize quality
                        {'fetch_format': 'auto'}   # Auto best format (WebP, etc.)
                    ]
                )

                # Clean up temp file if it was created
                if was_compressed and upload_path != file_path:
                    try:
                        os.unlink(upload_path)
                    except:
                        pass

                print(f"✅ Done!")
                uploaded += 1

            except Exception as e:
                print(f"❌ Failed!")
                print(f"   Error: {e}")
                failed += 1

    print(f"\n{'='*60}")
    print(f"✅ Uploaded: {uploaded}")
    if compressed_count > 0:
        print(f"📦 Compressed: {compressed_count}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎉 Wedding Photo Uploader to Cloudinary")
    print("="*60)

    # Upload party photos
    party_dir = "wedding/static/wedding/images/party"
    if os.path.exists(party_dir):
        upload_directory(party_dir, "wedding/party")
    else:
        print(f"\n⚠️  Party photos directory not found: {party_dir}")

    # Upload location photos
    locations_dir = "wedding/static/wedding/images/locations"
    if os.path.exists(locations_dir):
        upload_directory(locations_dir, "wedding/locations")
    else:
        print(f"\n⚠️  Locations photos directory not found: {locations_dir}")

    print("\n" + "="*60)
    print("✨ All done! Photos are now on Cloudinary.")
    print("🌐 View them at: https://cloudinary.com/console/media_library")
    print("="*60 + "\n")
