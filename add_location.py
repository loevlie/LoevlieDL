#!/usr/bin/env python
"""
Helper script to add wedding locations to the database.
Run with: python add_location.py

This makes it easy to add locations one at a time with all the details.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoevlieDL.settings')
django.setup()

from wedding.models import Location

def add_location(
    location_name,
    city,
    state_country,
    latitude,
    longitude,
    description,
    significance,
    date_visited="",
    order=0,
    photo_path=None
):
    """Add a location to the database."""

    location, created = Location.objects.update_or_create(
        location_name=location_name,
        city=city,
        defaults={
            'state_country': state_country,
            'latitude': latitude,
            'longitude': longitude,
            'description': description,
            'significance': significance,
            'date_visited': date_visited,
            'order': order,
            'is_active': True,
        }
    )

    if created:
        print(f"✓ Created: {location_name}")
    else:
        print(f"↻ Updated: {location_name}")

    return location


if __name__ == "__main__":
    print("Adding wedding locations...\n")

    # Example - we'll add locations here as you provide details
    # Morgantown - Where we met
    add_location(
        location_name="West Virginia University",
        city="Morgantown",
        state_country="West Virginia",
        latitude=39.6498,
        longitude=-79.9545,
        description="Where we met as classmates in the same major and became friends before falling in love senior year.",
        significance="The place where our story began",
        date_visited="2018-2022",
        order=1
    )

    print("\n✓ Done! Locations added to database.")
    print("Run the dev server and check /wedding/our-story/ to see them on the map!")
