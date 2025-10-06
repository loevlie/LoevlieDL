# RSVP & Wedding Party Setup Guide

## 🎉 Wedding Party Photos

### Setup:

1. **Create a Google Drive folder** for wedding party photos
2. **Upload photos** - name them anything (photo1.png, photo2.png, etc.)
3. **Share the folder** publicly (Anyone with the link → Viewer)
4. **Get the folder ID** from the URL
5. **Run sync command:**
   ```bash
   ./sync_wedding_party_photos.sh YOUR_FOLDER_ID
   ```

### Result:
- Beautiful Pinterest-style masonry collage
- 4 columns on desktop, 2 on tablet, 1 on mobile
- Hover effects with shadows
- Automatic responsive layout

### Updating Photos:
1. Cait adds photos to Google Drive
2. You run: `./sync_wedding_party_photos.sh FOLDER_ID`
3. Photos automatically appear in the collage!

---

## 💌 RSVP System

### How It Works Now:

**When someone submits an RSVP:**
1. ✅ Saved to database (backup)
2. 📧 Email sent to: `loevliedenny@gmail.com`
3. Email includes all details:
   - Name, email, phone
   - Attending status
   - Number of guests
   - Dietary restrictions
   - Song request
   - Message

### Viewing RSVPs:

**Option 1: Django Admin**
- Go to: `www.loevliedl.com/admin`
- Click "RSVPs"
- View, filter, search all responses

**Option 2: Export to Google Sheets**
```bash
python manage.py sync_rsvps_to_sheet
```
This creates a CSV file you can upload to Google Sheets.

### Email Setup:
Your email settings are already configured in `settings.py`:
- From: `loevliedenny@gmail.com`
- To: `loevliedenny@gmail.com`
- SMTP: Gmail

The email will work on your server (PythonAnywhere has it configured).

---

## 📧 Adding Cait's Email to Notifications

Edit `wedding/views.py` line 127 to add both emails:

```python
send_mail(
    subject,
    message,
    settings.DEFAULT_FROM_EMAIL,
    ['loevliedenny@gmail.com', 'cait@example.com'],  # Add Cait's email here
    fail_silently=True,
)
```

---

## 📱 Text/SMS Notifications (Optional)

To add SMS notifications, you'd need to:

1. **Sign up for Twilio** (or similar service)
2. **Add to requirements.txt:**
   ```
   twilio==8.2.0
   ```
3. **Update views.py** to send SMS after email

Would you like me to set up SMS notifications too?

---

## Quick Commands Reference:

```bash
# Sync wedding party photos
./sync_wedding_party_photos.sh FOLDER_ID

# Export RSVPs to CSV
python manage.py sync_rsvps_to_sheet

# Import locations from Google Sheet
python manage.py import_from_google_sheet SHEET_ID

# Sync location photos
./sync_wedding_photos.sh FOLDER_ID
```

---

## Testing RSVP:

1. Go to: `http://localhost:8000/wedding/rsvp/`
2. Fill out the form
3. Submit
4. Check your email! (On server only - won't work locally without SMTP setup)

---

## Next Steps:

1. **Upload party photos** to Google Drive
2. **Run sync** to display them
3. **Test an RSVP** on the live server
4. **Share Google Drive folders** with Cait so she can manage photos

Everything is set up for easy collaboration! 🎊
