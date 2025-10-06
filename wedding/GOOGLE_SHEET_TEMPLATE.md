# Google Sheet Template for Wedding Locations

## Setup Instructions

### 1. Create a New Google Sheet

Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet.

### 2. Add Column Headers (Row 1)

Copy these exact column names into the first row:

| location_name | city | state_country | latitude | longitude | description | significance | date_visited | order | photo_filename |

### 3. Fill in Your Data

Example rows:

| location_name | city | state_country | latitude | longitude | description | significance | date_visited | order | photo_filename |
|---------------|------|---------------|----------|-----------|-------------|--------------|--------------|-------|----------------|
| West Virginia University | Morgantown | West Virginia | 39.6498 | -79.9545 | Where we met as classmates and fell in love senior year. | The place where our story began | 2018-2022 | 1 | morgantown.jpg |
| The Aviary | Pittsburgh | Pennsylvania | 40.4406 | -79.9959 | Our home city where we built our life together. | Where we chose to build our future | 2022-Present | 2 | pittsburgh.jpg |

### 4. Get Coordinates

Use [LatLong.net](https://www.latlong.net/) or Google Maps:
- Search for the location
- Right-click on the map
- Click the coordinates to copy them

### 5. Share the Sheet

1. Click "Share" button (top right)
2. Under "General access" select **"Anyone with the link"**
3. Make sure it's set to **"Viewer"** (so they can view but you control editing)
4. Copy the link

### 6. Get the Sheet ID

From your Google Sheet URL:
```
https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J/edit
                                        ^^^^^^^^^^^^^^^^^^^^
                                        This is your SHEET_ID
```

### 7. Import to Django

Run this command locally:
```bash
python manage.py import_from_google_sheet YOUR_SHEET_ID
```

To replace all existing locations:
```bash
python manage.py import_from_google_sheet YOUR_SHEET_ID --clear
```

## Column Descriptions

- **location_name**: Name of the place (e.g., "West Virginia University", "Eiffel Tower")
- **city**: City name (e.g., "Morgantown", "Paris")
- **state_country**: State (US) or Country (e.g., "West Virginia", "France")
- **latitude**: Latitude coordinate (decimal format)
- **longitude**: Longitude coordinate (decimal format)
- **description**: Your story/memory from this place (2-4 sentences)
- **significance**: Why this place is special (1 sentence)
- **date_visited**: When you visited (flexible format: "2022", "Summer 2023", etc.)
- **order**: Display order on map (1, 2, 3... in chronological order)
- **photo_filename**: Name of photo file (e.g., "morgantown.jpg") - add to wedding/static/wedding/images/locations/

## Photo Setup

1. Rename your photos to match the `photo_filename` in the sheet
2. Add them to: `wedding/static/wedding/images/locations/`
3. Recommended format: `cityname.jpg` (e.g., `morgantown.jpg`, `paris.jpg`)
4. Images will show in the popup when clicking map markers

## Tips

- You and your partner can both edit the Google Sheet
- Run the import command whenever you update the sheet
- Keep the sheet shared with "Anyone with the link" for the command to work
- Order numbers help display locations chronologically (1 = first, 2 = second, etc.)

## Sample Google Sheet

I recommend starting with just 2-3 locations to test, then adding more!
