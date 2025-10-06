"""
Management command to import locations from a Google Sheet.

Setup:
1. Create a Google Sheet with the following columns:
   location_name, city, state_country, latitude, longitude,
   description, significance, date_visited, order, photo_filename

2. Share the Google Sheet publicly (Anyone with the link can view)

3. Get the sheet ID from the URL:
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit

4. Run: python manage.py import_from_google_sheet SHEET_ID

Usage:
    python manage.py import_from_google_sheet YOUR_SHEET_ID
"""

from django.core.management.base import BaseCommand
from wedding.models import Location
import csv
import urllib.request


class Command(BaseCommand):
    help = 'Import locations from a Google Sheet'

    def add_arguments(self, parser):
        parser.add_argument('sheet_id', type=str, help='Google Sheet ID')
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing locations before importing',
        )

    def handle(self, *args, **options):
        sheet_id = options['sheet_id']

        # Google Sheets CSV export URL
        csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'

        self.stdout.write(f'Fetching data from Google Sheet...')
        self.stdout.write(f'URL: {csv_url}\n')

        try:
            # Fetch the CSV data
            response = urllib.request.urlopen(csv_url)
            csv_data = response.read().decode('utf-8')

            # Parse CSV
            csv_reader = csv.DictReader(csv_data.splitlines())

            # Clear existing locations if requested
            if options['clear']:
                count = Location.objects.count()
                Location.objects.all().delete()
                self.stdout.write(self.style.WARNING(f'Deleted {count} existing locations'))

            created_count = 0
            updated_count = 0
            error_count = 0

            for row_num, row in enumerate(csv_reader, start=2):
                try:
                    # Skip empty rows
                    if not row.get('location_name') or not row.get('location_name').strip():
                        continue

                    # Get photo base name (e.g., 'morgantown' from 'morgantown.png' or just 'morgantown')
                    photo_filename = row.get('photo_filename', '').strip()
                    photo_base_name = ''
                    if photo_filename:
                        # Remove extension to get base name
                        photo_base_name = photo_filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')

                    # Create or update location
                    location, created = Location.objects.update_or_create(
                        location_name=row['location_name'].strip(),
                        city=row['city'].strip(),
                        defaults={
                            'state_country': row.get('state_country', '').strip(),
                            'latitude': float(row.get('latitude', 0)),
                            'longitude': float(row.get('longitude', 0)),
                            'description': row.get('description', '').strip(),
                            'significance': row.get('significance', '').strip(),
                            'date_visited': row.get('date_visited', '').strip(),
                            'order': int(row.get('order', 0)),
                            'photo_base_name': photo_base_name,
                            'is_active': True,
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Created: {location.location_name}')
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'↻ Updated: {location.location_name}')
                        )

                    # Note about photo if filename is provided
                    if photo_filename:
                        self.stdout.write(
                            f'   Photo: {photo_filename} (add to wedding/static/wedding/images/locations/)'
                        )

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'✗ Error on row {row_num}: {str(e)}')
                    )
                    self.stdout.write(self.style.ERROR(f'   Row data: {row}'))

            # Summary
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS(f'Import completed!'))
            self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
            self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count}'))
            if error_count > 0:
                self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))

        except urllib.error.HTTPError as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to fetch Google Sheet. Error: {e}')
            )
            self.stdout.write(
                self.style.ERROR('Make sure the sheet is shared publicly (Anyone with the link can view)')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to import: {str(e)}'))
