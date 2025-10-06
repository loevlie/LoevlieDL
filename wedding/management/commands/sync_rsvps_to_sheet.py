"""
Management command to sync RSVPs to a Google Sheet.

Setup:
1. Create a Google Sheet for RSVPs
2. Add these column headers in row 1:
   First Name | Last Name | Email | Phone | Attending | Number of Guests |
   Guest Names | Dietary Restrictions | Song Request | Message | Submitted At

3. Share the sheet publicly (for writing, you'll need Google Sheets API)
   OR use the simpler method: just run this command periodically to export

Usage:
    python manage.py sync_rsvps_to_sheet

This will create a CSV file you can import to Google Sheets.
"""

from django.core.management.base import BaseCommand
from wedding.models import RSVP
import csv
from datetime import datetime


class Command(BaseCommand):
    help = 'Export RSVPs to CSV for Google Sheets'

    def handle(self, *args, **options):
        # Create CSV filename with timestamp
        filename = f'rsvps_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

        rsvps = RSVP.objects.all().order_by('-submitted_at')

        self.stdout.write(f'Exporting {rsvps.count()} RSVPs...\n')

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write headers
            writer.writerow([
                'First Name', 'Last Name', 'Email', 'Phone',
                'Attending', 'Number of Guests', 'Guest Names',
                'Dietary Restrictions', 'Song Request', 'Message',
                'Submitted At'
            ])

            # Write data
            for rsvp in rsvps:
                writer.writerow([
                    rsvp.first_name,
                    rsvp.last_name,
                    rsvp.email,
                    rsvp.phone,
                    rsvp.get_attendance_display(),
                    rsvp.number_of_guests,
                    rsvp.guest_names,
                    rsvp.dietary_restrictions,
                    rsvp.song_request,
                    rsvp.message,
                    rsvp.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                ])

        self.stdout.write(self.style.SUCCESS(f'\n✓ Exported to: {filename}'))
        self.stdout.write('\nTo import to Google Sheets:')
        self.stdout.write('1. Open your Google Sheet')
        self.stdout.write('2. File → Import → Upload')
        self.stdout.write(f'3. Upload {filename}')
        self.stdout.write('4. Choose "Replace current sheet"\n')
