# Using Cloudinary for Wedding Photos

Cloudinary is a free image hosting service (25GB free tier) that will:
- Host your photos externally (no server storage used)
- Automatically optimize and resize images
- Serve images fast via CDN
- Handle thumbnails automatically

---

## Step 1: Sign Up for Cloudinary

1. Go to: https://cloudinary.com/users/register/free
2. Sign up with your email
3. After signup, you'll see your **Dashboard** with:
   - **Cloud Name** (e.g., `denny-wedding`)
   - **API Key**
   - **API Secret**

**Keep these credentials handy!**

---

## Step 2: Install Cloudinary Python Library

On both local and production:

```bash
pip install cloudinary
# or
pip3 install --user cloudinary
```

Add to `requirements.txt`:
```
cloudinary==1.36.0
```

---

## Step 3: Configure Django Settings

Add to your `LoevlieDL/settings.py`:

```python
# Cloudinary Configuration
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name = "YOUR_CLOUD_NAME",  # From Cloudinary dashboard
    api_key = "YOUR_API_KEY",
    api_secret = "YOUR_API_SECRET",
    secure = True
)

# Cloudinary folder structure
CLOUDINARY_WEDDING_PARTY_FOLDER = "wedding/party"
CLOUDINARY_WEDDING_LOCATIONS_FOLDER = "wedding/locations"
```

**Security Note:** For production, put credentials in environment variables:

```python
# Better approach for production
import os

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)
```

---

## Step 4: Upload Photos to Cloudinary

### Option A: Use Cloudinary Web Interface (Easiest)

1. Log into Cloudinary dashboard
2. Click **Media Library**
3. Create folders: `wedding/party` and `wedding/locations`
4. Drag and drop your photos into each folder
5. Done! Photos are now hosted on Cloudinary

### Option B: Upload Script (Automated)

Create a script to upload from your local folders:

```python
# upload_to_cloudinary.py
import cloudinary
import cloudinary.uploader
import os
from pathlib import Path

cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    secure=True
)

def upload_directory(local_dir, cloudinary_folder):
    """Upload all images from local directory to Cloudinary folder."""
    if not os.path.exists(local_dir):
        print(f"Directory not found: {local_dir}")
        return

    print(f"\nUploading from: {local_dir}")
    print(f"To Cloudinary folder: {cloudinary_folder}")
    print("-" * 60)

    for filename in os.listdir(local_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(local_dir, filename)

            try:
                result = cloudinary.uploader.upload(
                    file_path,
                    folder=cloudinary_folder,
                    resource_type="image",
                    overwrite=True,
                    transformation=[
                        {'quality': 'auto:good'},  # Auto optimize quality
                        {'fetch_format': 'auto'}   # Auto best format (WebP, etc.)
                    ]
                )
                print(f"✓ Uploaded: {filename} -> {result['secure_url']}")
            except Exception as e:
                print(f"✗ Failed to upload {filename}: {e}")

if __name__ == "__main__":
    # Upload party photos
    upload_directory(
        "wedding/static/wedding/images/party",
        "wedding/party"
    )

    # Upload location photos
    upload_directory(
        "wedding/static/wedding/images/locations",
        "wedding/locations"
    )

    print("\nDone! Photos are now on Cloudinary.")
```

Run it:
```bash
python upload_to_cloudinary.py
```

---

## Step 5: Update Your Views to Use Cloudinary URLs

Instead of scanning local directories, fetch photos from Cloudinary:

```python
# wedding/views.py

def party_photos_api(request):
    """API endpoint to list all photos from Cloudinary"""
    import cloudinary.api
    from django.http import JsonResponse

    try:
        # Get all images from Cloudinary folder
        result = cloudinary.api.resources(
            type="upload",
            prefix="wedding/party/",
            max_results=500
        )

        photos = []
        for resource in result.get('resources', []):
            # Cloudinary automatically handles thumbnails with transformations
            photos.append({
                'filename': resource['public_id'].split('/')[-1],
                'thumb': cloudinary.CloudinaryImage(resource['public_id']).build_url(
                    width=600,
                    height=600,
                    crop='limit',
                    quality='auto:good',
                    fetch_format='auto'
                ),
                'full': cloudinary.CloudinaryImage(resource['public_id']).build_url(
                    quality='auto:best',
                    fetch_format='auto'
                )
            })

        return JsonResponse({'photos': photos}, safe=False)

    except Exception as e:
        print(f"Error fetching from Cloudinary: {e}")
        return JsonResponse({'photos': []}, safe=False)
```

Update the JavaScript to use full-res URLs:

```javascript
// In wedding_party.html
img.src = photo.thumb;  // Use thumb URL
img.dataset.fullRes = photo.full;  // Use full URL
```

---

## Step 6: Update Locations API Similarly

```python
def locations_api(request):
    """API endpoint for location data with Cloudinary photos"""
    import cloudinary
    from django.http import JsonResponse

    locations = Location.objects.filter(is_active=True)
    locations_list = []

    for location in locations:
        # Build Cloudinary URLs for this location's photos
        photo_urls = []
        if location.photo_base_name:
            # Try to get matching photos from Cloudinary
            try:
                result = cloudinary.api.resources(
                    type="upload",
                    prefix=f"wedding/locations/{location.photo_base_name}",
                    max_results=10
                )
                for resource in result.get('resources', []):
                    photo_urls.append(
                        cloudinary.CloudinaryImage(resource['public_id']).build_url(
                            quality='auto:good',
                            fetch_format='auto'
                        )
                    )
            except:
                pass

        locations_list.append({
            'id': location.id,
            'location_name': location.location_name,
            'photos': photo_urls,
            # ... other fields
        })

    return JsonResponse({'locations': locations_list}, safe=False)
```

---

## Benefits of Using Cloudinary

✅ **No server storage used** - Photos hosted externally
✅ **Automatic optimization** - Cloudinary serves WebP, optimized quality
✅ **Auto thumbnails** - Just add `width=600` to URL
✅ **CDN delivery** - Fast loading worldwide
✅ **Free 25GB** - Way more than PythonAnywhere free tier
✅ **No sync scripts needed** - Just upload once via web interface or script

---

## Workflow Going Forward

1. **Add new photos:** Upload to Cloudinary web interface (drag & drop)
2. **That's it!** Photos immediately appear on your site
3. **No deployments needed** for new photos

---

## Quick Setup Summary

```bash
# 1. Install
pip install cloudinary

# 2. Add to settings.py (with your credentials)

# 3. Upload photos to Cloudinary (web interface or script)

# 4. Update views.py to fetch from Cloudinary

# 5. Deploy updated code

# 6. Done! No storage issues on PythonAnywhere
```

---

## Cost Comparison

| Option | Storage | Cost |
|--------|---------|------|
| PythonAnywhere Free | 512MB | Free (too small) |
| PythonAnywhere Hacker | 1GB | $5/month (still tight) |
| **Cloudinary Free** | **25GB** | **Free** ✅ |

Cloudinary is the clear winner for your use case!
