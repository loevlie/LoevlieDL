#!/bin/bash
# Sync wedding party photos from Google Drive
#
# Usage: ./sync_wedding_party_photos.sh GOOGLE_DRIVE_FOLDER_ID

if [ -z "$1" ]; then
    echo "Error: Please provide Google Drive folder ID"
    echo "Usage: ./sync_wedding_party_photos.sh FOLDER_ID"
    exit 1
fi

FOLDER_ID=$1
TARGET_DIR="wedding/static/wedding/images/party"

echo "🎉 Syncing wedding party photos from Google Drive..."
echo "Folder ID: $FOLDER_ID"
echo "Target: $TARGET_DIR"
echo ""

# Create target directory if it doesn't exist
mkdir -p $TARGET_DIR

# Download folder contents
echo "📥 Downloading photos..."
gdown --folder "https://drive.google.com/drive/folders/$FOLDER_ID" -O "$TARGET_DIR" --remaining-ok

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Photos synced successfully!"
    echo "📁 Location: $TARGET_DIR"
    echo ""
    echo "Photos will be displayed in a cool collage on the wedding party page!"
else
    echo ""
    echo "❌ Error downloading photos"
fi
