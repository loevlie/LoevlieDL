"""
Management command to import locations from an XLSX file.

Usage:
    python manage.py import_locations path/to/locations.xlsx
"""

from django.core.management.base import BaseCommand
from wedding.models import Location
import openpyxl
import os


class Command(BaseCommand):
    help = 'Import locations from an XLSX file'

    def add_arguments(self, parser):
        parser.add_argument('xlsx_file', type=str, help='Path to the XLSX file')
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing locations before importing',
        )

    def handle(self, *args, **options):
        xlsx_file = options['xlsx_file']

        if not os.path.exists(xlsx_file):
            self.stdout.write(self.style.ERROR(f'File not found: {xlsx_file}'))
            return

        try:
            workbook = openpyxl.load_workbook(xlsx_file)
            sheet = workbook.active

            # Clear existing locations if requested
            if options['clear']:
                count = Location.objects.count()
                Location.objects.all().delete()
                self.stdout.write(self.style.WARNING(f'Deleted {count} existing locations'))

            # Expected columns: location_name, city, state_country, latitude, longitude,
            #                   description, date_visited, significance, order
            headers = [cell.value for cell in sheet[1]]
            self.stdout.write(f'Headers found: {headers}')

            created_count = 0
            updated_count = 0
            error_count = 0

            for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    # Map row values to dictionary
                    row_data = dict(zip(headers, row))

                    # Skip empty rows
                    if not row_data.get('location_name'):
                        continue

                    # Check if location already exists (by name and city)
                    location, created = Location.objects.update_or_create(
                        location_name=row_data.get('location_name'),
                        city=row_data.get('city'),
                        defaults={
                            'state_country': row_data.get('state_country', ''),
                            'latitude': row_data.get('latitude', 0),
                            'longitude': row_data.get('longitude', 0),
                            'description': row_data.get('description', ''),
                            'date_visited': row_data.get('date_visited', ''),
                            'significance': row_data.get('significance', ''),
                            'order': row_data.get('order', 0),
                            'is_active': row_data.get('is_active', True),
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

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'✗ Error on row {row_num}: {str(e)}')
                    )

            # Summary
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS(f'Import completed!'))
            self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
            self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count}'))
            if error_count > 0:
                self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to import: {str(e)}'))
