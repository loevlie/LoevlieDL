"""
Management command to download photos from a shared Google Drive folder.

Setup:
1. Create a folder in Google Drive with your location photos
2. Name photos to match your photo_filename in the spreadsheet (e.g., morgantown.jpg)
3. Share the folder publicly:
   - Right click folder → Share → Anyone with the link → Viewer
4. Get the folder ID from the URL:
   https://drive.google.com/drive/folders/FOLDER_ID_HERE

Usage:
    python manage.py sync_photos_from_drive FOLDER_ID
"""

from django.core.management.base import BaseCommand
import urllib.request
import urllib.error
import os
from pathlib import Path
import re


class Command(BaseCommand):
    help = 'Download photos from a shared Google Drive folder'

    def add_arguments(self, parser):
        parser.add_argument('folder_id', type=str, help='Google Drive folder ID')

    def handle(self, *args, **options):
        folder_id = options['folder_id']

        # Path to save images
        base_dir = Path(__file__).resolve().parent.parent.parent
        images_dir = base_dir / 'static' / 'wedding' / 'images' / 'locations'
        images_dir.mkdir(parents=True, exist_ok=True)

        self.stdout.write(f'Syncing photos from Google Drive folder...')
        self.stdout.write(f'Folder ID: {folder_id}')
        self.stdout.write(f'Saving to: {images_dir}\n')

        # Google Drive folder view URL
        folder_url = f'https://drive.google.com/drive/folders/{folder_id}'

        try:
            # Fetch the folder page
            req = urllib.request.Request(folder_url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            response = urllib.request.urlopen(req)
            html = response.read().decode('utf-8')

            # Find all file IDs and names in the HTML
            # Pattern to match Google Drive file entries
            pattern = r'\["([^"]+)","([^"]+)".*?"image/jpeg"|"image/png"|"image/jpg"'
            matches = re.findall(pattern, html)

            if not matches:
                # Try alternative pattern
                pattern = r'data-id="([^"]+)".*?data-tooltip="([^"]+\.(jpg|jpeg|png))"'
                matches = re.findall(html, pattern)

            downloaded = 0
            skipped = 0
            errors = 0

            # More reliable method: Look for file IDs in the page source
            file_id_pattern = r'"([0-9A-Za-z_-]{25,})"'
            potential_file_ids = re.findall(file_id_pattern, html)

            # Get list of image files already in HTML
            image_pattern = r'(\w+\.(jpg|jpeg|png|JPG|JPEG|PNG))'
            image_filenames = re.findall(image_pattern, html)

            self.stdout.write(self.style.WARNING(
                f'Found {len(image_filenames)} image filename(s) in folder'
            ))

            for filename_match in image_filenames:
                filename = filename_match[0]

                self.stdout.write(f'Processing: {filename}')

                # Check if file already exists
                output_path = images_dir / filename
                if output_path.exists():
                    self.stdout.write(self.style.WARNING(f'  ⊙ Already exists: {filename}'))
                    skipped += 1
                    continue

                # Find corresponding file ID (this is tricky without API)
                # For now, we'll note this limitation
                self.stdout.write(self.style.WARNING(
                    f'  ⚠ Cannot auto-download without Google Drive API'
                ))
                self.stdout.write(
                    f'  → Manual download needed for: {filename}'
                )
                errors += 1

            # Summary
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.WARNING('⚠ Google Drive API Required'))
            self.stdout.write(self.style.WARNING(
                'Automatic photo download requires Google Drive API setup.'
            ))
            self.stdout.write('\n' + self.style.SUCCESS('Alternative: Manual Download'))
            self.stdout.write('1. Open your Google Drive folder')
            self.stdout.write('2. Select all images')
            self.stdout.write('3. Right-click → Download')
            self.stdout.write(f'4. Extract and copy to: {images_dir}')
            self.stdout.write('\nOr use the simpler method below!')

        except urllib.error.HTTPError as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to access Google Drive folder. Error: {e}')
            )
            self.stdout.write(
                self.style.ERROR('Make sure the folder is shared publicly (Anyone with the link can view)')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to sync: {str(e)}'))


        # Provide simpler alternative instructions
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('SIMPLER METHOD:'))
        self.stdout.write('Put photos in Google Drive folder, then:')
        self.stdout.write('1. Download entire folder as ZIP')
        self.stdout.write(f'2. Extract to: {images_dir}')
        self.stdout.write('3. Or use: wedding/sync_drive_photos.sh script (see below)\n')
