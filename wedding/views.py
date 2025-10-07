from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Location, WeddingPartyMember, RSVP
from .forms import RSVPForm


def home(request):
    """Wedding landing page with hero section"""
    context = {
        'bride_name': 'Caitlin Morrow',
        'groom_name': 'Dennis Loevlie',
        'wedding_date': 'September 5th, 2026',
        'wedding_location': 'Pittsburgh, PA',
    }
    return render(request, 'wedding/home.html', context)


def our_story(request):
    """Page displaying the couple's story"""
    story_text = """We met in undergrad as classmates in the same major, stayed friends,
    and finally started dating senior year. After graduation, we moved to Pittsburgh and
    began building a life we love—exploring neighborhoods, taking weekend trips, and finding
    'our' spots around the city. At home, we cook together and unwind with romantic comedies.
    From lecture halls to city streets, we're still choosing each other—and can't wait to
    celebrate with you."""

    context = {
        'story_text': story_text,
    }
    return render(request, 'wedding/our_story.html', context)


def wedding_party(request):
    """Display wedding party members with photos and carousel"""
    party_members = WeddingPartyMember.objects.filter(is_active=True)

    context = {
        'party_members': party_members,
        'bride_side': party_members.filter(side='bride'),
        'groom_side': party_members.filter(side='groom'),
    }
    return render(request, 'wedding/wedding_party.html', context)


def party_photos_api(request):
    """API endpoint to list all photos from Cloudinary"""
    import cloudinary.api

    try:
        # Get all images from Cloudinary wedding/party folder
        result = cloudinary.api.resources(
            type="upload",
            prefix="wedding/party/",
            max_results=500
        )

        photos = []
        for resource in result.get('resources', []):
            public_id = resource['public_id']
            filename = public_id.split('/')[-1]

            # Generate thumbnail URL (600px max, optimized)
            thumb_url = cloudinary.CloudinaryImage(public_id).build_url(
                width=600,
                height=600,
                crop='limit',
                quality='auto:good',
                fetch_format='auto'
            )

            # Generate full resolution URL (optimized)
            full_url = cloudinary.CloudinaryImage(public_id).build_url(
                quality='auto:best',
                fetch_format='auto'
            )

            photos.append({
                'filename': filename,
                'thumb': thumb_url,
                'full': full_url
            })

        return JsonResponse({'photos': sorted(photos, key=lambda x: x['filename'])}, safe=False)

    except Exception as e:
        print(f"Error fetching from Cloudinary: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'photos': []}, safe=False)


def our_journey(request):
    """Interactive map showing locations from the couple's journey"""
    locations = Location.objects.filter(is_active=True)

    context = {
        'locations': locations,
    }
    return render(request, 'wedding/our_journey.html', context)


def locations_api(request):
    """API endpoint for location data (used by the interactive map)"""
    import cloudinary.api

    locations = Location.objects.filter(is_active=True)

    locations_list = []
    for location in locations:
        # Get photos from Cloudinary for this location
        photo_urls = []

        if location.photo_base_name:
            try:
                # Search for photos matching this location's base name
                result = cloudinary.api.resources(
                    type="upload",
                    prefix=f"wedding/locations/{location.photo_base_name}",
                    max_results=10
                )

                for resource in result.get('resources', []):
                    public_id = resource['public_id']

                    # Progressive JPEG for incremental loading
                    photo_url = cloudinary.CloudinaryImage(public_id).build_url(
                        quality='auto:good',
                        fetch_format='auto',
                        flags='progressive'
                    )

                    photo_urls.append(photo_url)
            except Exception as e:
                print(f"Error fetching Cloudinary photos for {location.location_name}: {e}")

        locations_list.append({
            'id': location.id,
            'location_name': location.location_name,
            'city': location.city,
            'state_country': location.state_country,
            'latitude': float(location.latitude),
            'longitude': float(location.longitude),
            'description': location.description,
            'significance': location.significance,
            'date_visited': location.date_visited,
            'order': location.order,
            'photos': photo_urls,  # Array of Cloudinary photo URLs
        })

    return JsonResponse({'locations': locations_list}, safe=False)


def event_details(request):
    """Wedding event details page"""
    context = {
        'date': 'September 5th, 2026',
        'venue_name': 'The Aviary',
        'venue_address': 'Pittsburgh, PA',
        'ceremony_time': 'TBD',
        'reception_time': 'TBD',
    }
    return render(request, 'wedding/event_details.html', context)


def rsvp(request):
    """RSVP form page"""
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp_obj = form.save()

            # Send email notification with Excel attachment
            try:
                from django.core.mail import EmailMessage
                from django.conf import settings
                from openpyxl import Workbook
                from openpyxl.styles import Font, PatternFill
                import io
                from datetime import datetime

                # Create Excel workbook with all RSVPs
                wb = Workbook()
                ws = wb.active
                ws.title = "RSVPs"

                # Add headers with styling
                headers = [
                    'First Name', 'Last Name', 'Email', 'Phone',
                    'Attending', 'Number of Guests', 'Guest Names',
                    'Dietary Restrictions', 'Song Request', 'Message',
                    'Submitted At'
                ]

                header_fill = PatternFill(start_color="C99B8A", end_color="C99B8A", fill_type="solid")
                header_font = Font(bold=True, color="FFFFFF")

                for col_num, header in enumerate(headers, 1):
                    cell = ws.cell(row=1, column=col_num, value=header)
                    cell.fill = header_fill
                    cell.font = header_font

                # Add all RSVP data
                rsvps = RSVP.objects.all().order_by('-submitted_at')
                for row_num, rsvp in enumerate(rsvps, 2):
                    ws.cell(row=row_num, column=1, value=rsvp.first_name)
                    ws.cell(row=row_num, column=2, value=rsvp.last_name)
                    ws.cell(row=row_num, column=3, value=rsvp.email)
                    ws.cell(row=row_num, column=4, value=rsvp.phone)
                    ws.cell(row=row_num, column=5, value=rsvp.get_attendance_display())
                    ws.cell(row=row_num, column=6, value=rsvp.number_of_guests)
                    ws.cell(row=row_num, column=7, value=rsvp.guest_names)
                    ws.cell(row=row_num, column=8, value=rsvp.dietary_restrictions)
                    ws.cell(row=row_num, column=9, value=rsvp.song_request)
                    ws.cell(row=row_num, column=10, value=rsvp.message)
                    ws.cell(row=row_num, column=11, value=rsvp.submitted_at.strftime('%Y-%m-%d %H:%M:%S'))

                # Adjust column widths
                for col in ws.columns:
                    max_length = 0
                    column = col[0].column_letter
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    ws.column_dimensions[column].width = adjusted_width

                # Save to bytes
                excel_file = io.BytesIO()
                wb.save(excel_file)
                excel_file.seek(0)

                # Create email with attachment
                subject = f'New Wedding RSVP: {rsvp_obj.first_name} {rsvp_obj.last_name}'
                message = f"""
New RSVP Received!

Name: {rsvp_obj.first_name} {rsvp_obj.last_name}
Email: {rsvp_obj.email}
Phone: {rsvp_obj.phone}
Attending: {rsvp_obj.get_attendance_display()}
Number of Guests: {rsvp_obj.number_of_guests}
Guest Names: {rsvp_obj.guest_names}
Dietary Restrictions: {rsvp_obj.dietary_restrictions}
Song Request: {rsvp_obj.song_request}
Message: {rsvp_obj.message}

Submitted: {rsvp_obj.submitted_at}

---
See attached Excel file for all RSVPs.
                """

                email = EmailMessage(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['loevliedenny@gmail.com', 'caitbmorrow@gmail.com'],
                )

                # Attach Excel file
                filename = f'wedding_rsvps_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
                email.attach(filename, excel_file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

                email.send(fail_silently=False)

            except Exception as e:
                print(f"Error sending email: {e}")
                import traceback
                traceback.print_exc()

            messages.success(request, 'Thank you for your RSVP! We can\'t wait to celebrate with you!')
            return redirect('wedding:rsvp')
    else:
        form = RSVPForm()

    context = {
        'form': form,
    }
    return render(request, 'wedding/rsvp.html', context)


def registry(request):
    """Registry information page"""
    context = {
        'registry_links': [
            # Add registry links here as needed
        ]
    }
    return render(request, 'wedding/registry.html', context)
