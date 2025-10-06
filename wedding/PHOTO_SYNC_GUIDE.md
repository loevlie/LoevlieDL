# Photo Sync from Google Drive

## Simple Method (Recommended for Cait)

### Setup Once:

1. **Create a Google Drive folder** for wedding location photos
2. **Share it publicly**:
   - Right-click folder → Share
   - Change to "Anyone with the link" → Viewer
3. **Name photos** to match the `photo_filename` column in your spreadsheet
   - Examples: `morgantown.jpg`, `pittsburgh.jpg`, `amsterdam.jpg`

### When Adding New Photos:

**Option A: Manual Download (Easiest)**
1. Open the Google Drive folder
2. Select all photos (or just new ones)
3. Right-click → Download
4. Extract the ZIP file
5. Copy photos to: `wedding/static/wedding/images/locations/`
6. Run: `python manage.py collectstatic` (on server)

**Option B: Using rclone (One-time setup, then automatic)**

Install rclone once:
```bash
pip install gdown
```

Then create a simple sync script:

```bash
# wedding/sync_photos.sh
#!/bin/bash
DRIVE_FOLDER_ID="YOUR_FOLDER_ID_HERE"
LOCAL_PATH="wedding/static/wedding/images/locations/"

echo "Downloading photos from Google Drive..."
gdown --folder https://drive.google.com/drive/folders/$DRIVE_FOLDER_ID -O $LOCAL_PATH
echo "✓ Photos synced!"
```

Make it executable:
```bash
chmod +x wedding/sync_photos.sh
```

Run it:
```bash
./wedding/sync_photos.sh
```

## For Cait (Non-Technical Steps):

1. **Upload photos to the shared Google Drive folder**
   - Name them exactly as they appear in the spreadsheet
   - Example: If spreadsheet says `morgantown.jpg`, name your file `morgantown.jpg`

2. **Tell Dennis** "I added new photos!"

3. Dennis runs: `./wedding/sync_photos.sh` (or manually downloads)

That's it! The photos will appear on the map.

## Photo Naming Convention

Match these to your spreadsheet's `photo_filename` column:

```
morgantown.jpg       (West Virginia University)
pittsburgh.jpg       (Pittsburgh)
sandiego.jpg         (San Diego)
boston.jpg           (Boston)
barharbor.jpg        (Bar Harbor)
oceancity.jpg        (Ocean City)
salem.jpg            (Salem)
nantucket.jpg        (Nantucket)
chicago.jpg          (Chicago)
denver.jpg           (Denver)
amsterdam.jpg        (Amsterdam)
berlin.jpg           (Berlin)
oslo.jpg             (Oslo)
flekkeroy.jpg        (Flekkerøy)
kristiansand.jpg     (Kristiansand)
grimstad.jpg         (Grimstad)
london.jpg           (London)
liverpool.jpg        (Liverpool)
positano.jpg         (Positano)
cancun.jpg           (Cancun)
```

## Tips

- Use lowercase for filenames
- No spaces in filenames (use hyphens: `bar-harbor.jpg`)
- JPG or PNG format works best
- Keep photos under 5MB each for faster loading
- Square or landscape orientation works best

## Troubleshooting

**Photo not showing on map?**
1. Check filename matches exactly (including .jpg extension)
2. Make sure photo is in: `wedding/static/wedding/images/locations/`
3. Run: `python manage.py collectstatic` on server
4. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)

**Getting folder ID from Google Drive:**
```
https://drive.google.com/drive/folders/1A2B3C4D5E6F7G8H9I0J
                                        ^^^^^^^^^^^^^^^^^^^^
                                        This is the folder ID
```
