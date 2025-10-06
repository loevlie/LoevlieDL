# Deployment Guide - Wedding Website to Production

## Step 1: Push Code to GitHub

```bash
# Make sure you're in the project directory
cd /home/denny-loevlie/Wedding/LoevlieDL

# Add all changes
git add .

# Commit with a descriptive message
git commit -m "Complete wedding website with RSVP, photo galleries, and email notifications"

# Push to GitHub
git push origin main
```

## Step 2: Pull on Production Server (PythonAnywhere)

```bash
# SSH into PythonAnywhere or use their Bash console
cd ~/LoevlieDL

# Pull the latest changes
git pull origin main

# Install any new Python dependencies
pip install --user openpyxl Pillow

# Or if using pip3:
pip3 install --user openpyxl Pillow
```

## Step 3: Run Database Migrations

```bash
# Create migration files for any model changes
python manage.py makemigrations wedding

# Apply migrations to the database
python manage.py migrate

# If you get errors about existing tables, you may need to fake the initial migration:
# python manage.py migrate wedding --fake-initial
```

## Step 4: Collect Static Files

```bash
# Collect all static files (CSS, JS, images)
python manage.py collectstatic --noinput
```

## Step 5: Sync Photos from Google Drive

```bash
# Make the sync scripts executable (if not already)
chmod +x sync_wedding_photos.sh
chmod +x sync_wedding_party_photos.sh

# Sync location photos
./sync_wedding_photos.sh YOUR_LOCATION_FOLDER_ID

# Sync wedding party photos
./sync_wedding_party_photos.sh YOUR_PARTY_FOLDER_ID
```

**Note:** You'll need to have `gdown` installed on the server:
```bash
pip install --user gdown
# or
pip3 install --user gdown
```

## Step 6: Sync Location Data from Google Sheets

```bash
# Import locations from your Google Sheet
python manage.py import_from_google_sheet YOUR_SHEET_ID
```

## Step 7: Create Django Admin Superuser (if needed)

```bash
# Only if you haven't created one yet
python manage.py createsuperuser
```

## Step 8: Reload Web App

In PythonAnywhere:
1. Go to the **Web** tab
2. Click the **Reload** button for your web app
3. Check for any errors in the error log

## Step 9: Test Everything

1. **Visit the site:** `www.loevliedl.com/wedding/`
2. **Test RSVP:** Submit a test RSVP and check both emails (loevliedenny@gmail.com and caitbmorrow@gmail.com)
3. **Check photos:**
   - Location photos on "Our Story" page
   - Party photos on "Wedding Party" page
   - Click photos to view full resolution
4. **Test admin:** Visit `www.loevliedl.com/admin` and view RSVPs

## Step 10: Verify Photo Directories Exist

If photos don't show up, create the directories manually on the server:

```bash
mkdir -p ~/LoevlieDL/wedding/static/wedding/images/party
mkdir -p ~/LoevlieDL/wedding/static/wedding/images/locations
```

Then re-run the sync scripts (Step 5).

---

## Troubleshooting

### Email Not Sending
- Check your email settings in `settings.py` on the production server
- Make sure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are set correctly
- Check PythonAnywhere's SMTP restrictions

### Photos Not Showing
- Make sure sync scripts ran successfully
- Check file permissions: `chmod -R 755 wedding/static/wedding/images/`
- Run `collectstatic` again
- Check the error log in PythonAnywhere

### Database Errors
- Try: `python manage.py migrate wedding --fake-initial`
- Check that the database exists and is accessible

### Import Error: No module named 'openpyxl' or 'PIL'
- Install missing dependencies: `pip install --user openpyxl Pillow`

---

## Quick Command Summary

```bash
# On production server
cd ~/LoevlieDL
git pull origin main
pip install --user openpyxl Pillow gdown
python manage.py makemigrations wedding
python manage.py migrate
python manage.py collectstatic --noinput
./sync_wedding_photos.sh YOUR_LOCATION_FOLDER_ID
./sync_wedding_party_photos.sh YOUR_PARTY_FOLDER_ID
python manage.py import_from_google_sheet YOUR_SHEET_ID
# Then reload web app in PythonAnywhere dashboard
```

---

## Important Notes

- **Photos are NOT in git** - You must sync them using the scripts
- **Thumbnails are auto-generated** - They'll be created the first time someone visits the wedding party page
- **RSVP Excel files** - These are generated on-the-fly and emailed, not stored on the server
- **Database** - Your production database (MySQL) is separate from your local SQLite database

---

## Future Updates

When you make changes:
1. Commit and push to GitHub
2. Pull on production server
3. Run migrations if models changed
4. Collect static files if CSS/JS changed
5. Reload web app

No need to re-sync photos unless you've added new ones to Google Drive!
