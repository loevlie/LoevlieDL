from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Location model for the interactive relationship map
class Location(models.Model):
    location_name = models.CharField(max_length=200, help_text="Name of the location (e.g., 'West Virginia University')")
    city = models.CharField(max_length=100)
    state_country = models.CharField(max_length=100, help_text="State (for US) or Country")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(help_text="Story or memory from this location")
    photo = models.ImageField(upload_to='wedding/locations/', blank=True, null=True)
    photo_base_name = models.CharField(max_length=100, blank=True, help_text="Base name for photos (e.g., 'morgantown' for morgantown_1.png, morgantown_2.png)")
    date_visited = models.CharField(max_length=100, blank=True, help_text="When you visited (can be flexible format)")
    significance = models.CharField(max_length=200, help_text="Why this place is special")
    order = models.IntegerField(default=0, help_text="Order for chronological display")
    is_active = models.BooleanField(default=True, help_text="Show this location on the map")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'date_visited']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"{self.location_name} - {self.city}, {self.state_country}"

    def get_photo_urls(self):
        """
        Get all photo URLs for this location.
        Looks for files like: morgantown.png, morgantown_1.png, morgantown_2.png, etc.
        """
        import os
        from django.conf import settings

        if not self.photo_base_name:
            return []

        photos = []
        static_dir = os.path.join(settings.BASE_DIR, 'wedding', 'static', 'wedding', 'images', 'locations')

        if not os.path.exists(static_dir):
            return []

        # Look for all matching files
        for filename in os.listdir(static_dir):
            # Check if filename matches pattern: basename.ext or basename_N.ext
            base = self.photo_base_name.lower()
            name_lower = filename.lower()

            # Match: morgantown.png or morgantown_1.png, morgantown_2.png, etc.
            if (name_lower == f"{base}.png" or
                name_lower == f"{base}.jpg" or
                name_lower == f"{base}.jpeg" or
                name_lower.startswith(f"{base}_") and (
                    name_lower.endswith('.png') or
                    name_lower.endswith('.jpg') or
                    name_lower.endswith('.jpeg')
                )):
                photos.append(f"/static/wedding/images/locations/{filename}")

        return sorted(photos)  # Sort to get consistent order


# Wedding party member model
class WeddingPartyMember(models.Model):
    SIDE_CHOICES = [
        ('bride', 'Bride\'s Side'),
        ('groom', 'Groom\'s Side'),
    ]

    ROLE_CHOICES = [
        ('maid_of_honor', 'Maid of Honor'),
        ('best_man', 'Best Man'),
        ('bridesmaid', 'Bridesmaid'),
        ('groomsman', 'Groomsman'),
        ('flower_girl', 'Flower Girl'),
        ('ring_bearer', 'Ring Bearer'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    side = models.CharField(max_length=10, choices=SIDE_CHOICES)
    photo = models.ImageField(upload_to='wedding/party/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order in the gallery")
    bio = models.TextField(blank=True, help_text="Optional bio or fun fact")
    is_active = models.BooleanField(default=True, help_text="Include in wedding party display")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['side', 'order']
        verbose_name = 'Wedding Party Member'
        verbose_name_plural = 'Wedding Party Members'

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"


# RSVP model
class RSVP(models.Model):
    ATTENDANCE_CHOICES = [
        ('yes', 'Accept'),
        ('no', 'Decline'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)  # Now mandatory
    attendance = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    number_of_guests = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Total number attending (including yourself)"
    )
    guest_names = models.TextField(blank=True, help_text="Names of additional guests (deprecated - use Guest model)")
    dietary_restrictions = models.TextField(blank=True)
    song_request = models.CharField(max_length=200, blank=True, help_text="Song you'd love to hear at the reception")
    message = models.TextField(blank=True, help_text="Any message for the couple")
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'RSVP'
        verbose_name_plural = 'RSVPs'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_attendance_display()}"


# Guest model for additional guests in RSVP
class Guest(models.Model):
    rsvp = models.ForeignKey(RSVP, on_delete=models.CASCADE, related_name='guests')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    use_primary_phone = models.BooleanField(
        default=True,
        help_text="Can we use the primary contact's phone number to reach this guest?"
    )
    phone = models.CharField(max_length=20, blank=True, help_text="Only if different from primary contact")

    class Meta:
        ordering = ['id']
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Guest of {self.rsvp.first_name} {self.rsvp.last_name})"

    def get_contact_phone(self):
        """Get the phone number to use for this guest"""
        if self.use_primary_phone or not self.phone:
            return self.rsvp.phone
        return self.phone


# Wedding photo uploads from guests
class PhotoUpload(models.Model):
    uploaded_by_name = models.CharField(max_length=200, help_text="Name of person uploading")
    photo_url = models.URLField(help_text="Cloudinary URL of uploaded photo")
    caption = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, help_text="Show on public gallery")

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Photo Upload'
        verbose_name_plural = 'Photo Uploads'

    def __str__(self):
        return f"Photo by {self.uploaded_by_name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
