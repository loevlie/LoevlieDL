#!/bin/bash
# Sync wedding location photos from Google Drive
#
# Usage: ./sync_wedding_photos.sh GOOGLE_DRIVE_FOLDER_ID
#
# Get the folder ID from your shared Google Drive folder URL:
# https://drive.google.com/drive/folders/FOLDER_ID_HERE

if [ -z "$1" ]; then
    echo "Error: Please provide Google Drive folder ID"
    echo "Usage: ./sync_wedding_photos.sh FOLDER_ID"
    echo ""
    echo "Get folder ID from URL: https://drive.google.com/drive/folders/FOLDER_ID"
    exit 1
fi

FOLDER_ID=$1
TARGET_DIR="wedding/static/wedding/images/locations"

echo "🎉 Syncing wedding photos from Google Drive..."
echo "Folder ID: $FOLDER_ID"
echo "Target: $TARGET_DIR"
echo ""

# Create target directory if it doesn't exist
mkdir -p $TARGET_DIR

# Check if gdown is installed
if ! command -v gdown &> /dev/null; then
    echo "⚠️  gdown is not installed. Installing..."
    pip install gdown
fi

# Download folder contents
echo "📥 Downloading photos..."
gdown --folder "https://drive.google.com/drive/folders/$FOLDER_ID" -O "$TARGET_DIR" --remaining-ok

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Photos synced successfully!"
    echo "📁 Location: $TARGET_DIR"
    echo ""
    echo "Next steps:"
    echo "  1. Check photos are in: $TARGET_DIR"
    echo "  2. On server, run: python manage.py collectstatic"
    echo "  3. Restart your Django app"
else
    echo ""
    echo "❌ Error downloading photos"
    echo "Make sure the folder is shared publicly (Anyone with the link can view)"
fi
