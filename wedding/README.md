# Wedding Website Django App

A modern, elegant wedding website with a playful Pittsburgh/penguin theme, designed to integrate seamlessly with the existing LoevlieDL portfolio site.

**Wedding Details:** Dennis Loevlie & Cait Morrow
**Date:** September 5th, 2026
**Location:** The Aviary, Pittsburgh, PA
**URL:** www.loevliedl.com/wedding

---

## Features

- 🏠 **Home/Landing Page** - Hero section with wedding details
- 📖 **Our Story** - Couple's story with interactive journey map
- 👥 **Wedding Party** - Photo gallery with name carousel
- 🗺️ **Interactive Map** - Clickable penguin markers showing locations from the couple's journey
- 📅 **Event Details** - Venue, schedule, accommodations, travel info
- 💌 **RSVP Form** - Functional form with database storage
- 🎁 **Registry** - Registry links and information
- 🐧 **Penguin Theme** - Playful animations and Easter eggs throughout

---

## Installation & Deployment

### 1. On Your Server (PythonAnywhere)

#### Install Required Package

```bash
pip install openpyxl==3.0.9
```

This is the only new dependency needed for XLSX import functionality.

#### Run Migrations

```bash
cd /home/dloevlie/Wedding/LoevlieDL
python manage.py makemigrations wedding
python manage.py migrate wedding
```

#### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 2. Configuration (Already Done)

The following changes have been made to integrate the wedding app:

**LoevlieDL/settings.py:**
- Added `'wedding'` to `INSTALLED_APPS`

**LoevlieDL/urls.py:**
- Added `path('wedding/', include('wedding.urls'))` to urlpatterns

---

## File Structure

```
wedding/
├── README.md                          # This file
├── __init__.py
├── admin.py                           # Django admin configuration
├── apps.py                            # App configuration
├── forms.py                           # RSVP form
├── models.py                          # Location, WeddingPartyMember, RSVP models
├── urls.py                            # URL routing
├── views.py                           # View functions
├── management/
│   └── commands/
│       ├── __init__.py
│       ├── import_locations.py        # Import locations from XLSX
│       └── create_location_template.py # Generate sample XLSX
├── migrations/
│   └── (auto-generated)
├── static/
│   └── wedding/
│       ├── css/
│       │   └── wedding.css           # All wedding styling
│       ├── js/
│       │   └── wedding.js            # Interactive features
│       └── images/
│           └── (place wedding images here)
└── templates/
    └── wedding/
        ├── base.html                 # Base template with navigation
        ├── home.html                 # Landing page
        ├── our_story.html            # Story + interactive map
        ├── wedding_party.html        # Wedding party gallery
        ├── event_details.html        # Event information
        ├── rsvp.html                 # RSVP form
        └── registry.html             # Registry information
```

---

## Managing Content

### Django Admin

Access the admin at: `www.loevliedl.com/admin`

Three models are available:
1. **Locations** - Manage map locations
2. **Wedding Party Members** - Manage wedding party
3. **RSVPs** - View guest responses

### Adding Locations

#### Method 1: Django Admin (Manual)
1. Go to Admin → Locations → Add Location
2. Fill in all fields:
   - Location name, city, state/country
   - Latitude/longitude (use Google Maps to find coordinates)
   - Description, significance, date visited
   - Order (for chronological display)
   - Upload photo (optional)

#### Method 2: XLSX Import (Bulk)

1. **Create a template:**
   ```bash
   python manage.py create_location_template locations.xlsx
   ```

2. **Edit the XLSX file** with your location data. Required columns:
   - `location_name` - Name of the location
   - `city` - City name
   - `state_country` - State (US) or Country
   - `latitude` - Decimal latitude
   - `longitude` - Decimal longitude
   - `description` - Story/memory from this location
   - `date_visited` - When you visited
   - `significance` - Why it's special
   - `order` - Display order (0, 1, 2, etc.)
   - `is_active` - TRUE or FALSE

3. **Import the file:**
   ```bash
   python manage.py import_locations locations.xlsx
   ```

   To clear existing locations first:
   ```bash
   python manage.py import_locations locations.xlsx --clear
   ```

### Sample Locations Data

Here are the locations mentioned in your requirements:

**United States:**
- Morgantown, WV (39.6295, -79.9559) - West Virginia University
- Pittsburgh, PA (40.4406, -79.9959) - Home
- San Diego, CA (32.7157, -117.1611)
- Boston, MA (42.3601, -71.0589)
- Bar Harbor, ME (44.3876, -68.2039)
- Ocean City, MD (38.3365, -75.0849)
- Salem, MA (42.5195, -70.8967)
- Nantucket, MA (41.2835, -70.0995)
- Chicago, IL (41.8781, -87.6298)
- Denver, CO (39.7392, -104.9903)

**Europe:**
- Amsterdam, Netherlands (52.3676, 4.9041)
- Berlin, Germany (52.5200, 13.4050)
- Oslo, Norway (59.9139, 10.7522)
- Flekkerøy, Norway (58.0583, 8.0083)
- Kristiansand, Norway (58.1467, 7.9956)
- Grimstad, Norway (58.3405, 8.5934)
- London, UK (51.5074, -0.1278)
- Liverpool, UK (53.4084, -2.9916)
- Positano, Italy (40.6280, 14.4850)

**Mexico:**
- Cancun, Mexico (21.1619, -86.8515)

### Adding Wedding Party Members

1. Go to Admin → Wedding Party Members → Add
2. Fill in:
   - Name
   - Role (Maid of Honor, Best Man, Bridesmaid, Groomsman, etc.)
   - Side (Bride's Side or Groom's Side)
   - Upload photo
   - Bio (optional)
   - Display order

### Viewing RSVPs

1. Go to Admin → RSVPs
2. View all guest responses
3. Filter by attendance status
4. Export data as needed

---

## Customization

### Updating Wedding Details

Edit `wedding/views.py` to update:
- Names
- Wedding date
- Venue information
- Times
- Registry links

### Styling/Colors

Edit `wedding/static/wedding/css/wedding.css`:

```css
:root {
  --wedding-primary: #e75480;      /* Pink accent color */
  --wedding-secondary: #36454F;    /* Charcoal gray */
  --wedding-accent: #FFD700;       /* Gold */
}
```

### Penguin Easter Eggs

The site includes several playful penguin interactions:
- Clicking penguin emojis 3 times triggers a penguin party
- Random penguin waddles across the bottom
- RSVP "Yes" shows celebration penguins
- Hover effects on various elements

Edit `wedding/static/wedding/js/wedding.js` to modify or add interactions.

---

## URLs

All wedding pages are under the `/wedding/` path:

- `/wedding/` - Home page
- `/wedding/our-story/` - Our story with map
- `/wedding/party/` - Wedding party
- `/wedding/details/` - Event details
- `/wedding/rsvp/` - RSVP form
- `/wedding/registry/` - Registry
- `/wedding/api/locations/` - Location data API (for map)

---

## Testing Checklist

Before going live:

- [ ] Run migrations on server
- [ ] Collect static files
- [ ] Add at least 2-3 locations to test the map
- [ ] Add wedding party members with photos
- [ ] Test RSVP form submission
- [ ] Check all pages on mobile devices
- [ ] Verify map loads and markers are clickable
- [ ] Test navigation between pages
- [ ] Update event details with actual times
- [ ] Add registry links
- [ ] Test from different browsers

---

## Mobile Responsiveness

The site is fully responsive with breakpoints at:
- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: < 768px

All elements adapt appropriately including:
- Navigation collapses to hamburger menu
- Map height adjusts
- Cards stack vertically
- Font sizes scale down
- Touch-friendly buttons

---

## Production Notes

### Media Files

Wedding photos should be uploaded through Django admin. They will be stored in:
```
media/wedding/locations/  - Location photos
media/wedding/party/      - Wedding party photos
```

Make sure your server's media directory is properly configured and writable.

### Database

Uses the existing MySQL database configured in settings.py. Three new tables will be created:
- `wedding_location`
- `wedding_weddingpartymember`
- `wedding_rsvp`

### Security

- CSRF protection enabled on RSVP form
- Admin access restricted to authenticated users
- No sensitive information exposed in templates
- reCAPTCHA already configured in main site (can be added to RSVP if needed)

---

## Support & Maintenance

### Common Tasks

**Update story text:**
Edit `wedding/views.py` → `our_story()` function

**Change venue details:**
Edit `wedding/views.py` → `event_details()` function

**Modify navigation:**
Edit `wedding/templates/wedding/base.html`

**Add countdown timer:**
Uncomment the countdown section in `wedding/static/wedding/js/wedding.js`

### Troubleshooting

**Map not loading:**
- Check that Leaflet CSS/JS CDN links are accessible
- Verify location data exists in database
- Check browser console for JavaScript errors

**RSVP form not submitting:**
- Verify CSRF token is present
- Check form validation
- Review server logs for errors

**Static files not loading:**
- Run `python manage.py collectstatic`
- Verify STATIC_URL and STATIC_ROOT settings
- Check file permissions

---

## Future Enhancements

Possible additions:
- Photo gallery page
- Guest messages/guestbook
- Live countdown timer on homepage
- Photo upload feature for guests
- Email notifications for new RSVPs
- Calendar export (.ics file)
- Directions/transportation page
- FAQ section

---

## Credits

Built with:
- Django 3.1.5
- Bootstrap 4.4.1
- Leaflet.js (for maps)
- Font Awesome (for icons)
- Custom CSS & JavaScript

Theme: Pittsburgh Penguin 🐧💕
