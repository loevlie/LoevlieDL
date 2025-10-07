from django.urls import path
from . import views

app_name = 'wedding'

urlpatterns = [
    path('', views.home, name='home'),
    path('our-story/', views.our_story, name='our_story'),
    path('party/', views.wedding_party, name='wedding_party'),
    path('our-journey/', views.our_journey, name='our_journey'),
    path('details/', views.event_details, name='event_details'),
    path('rsvp/', views.rsvp, name='rsvp'),
    path('registry/', views.registry, name='registry'),
    path('photos/upload/', views.photo_upload, name='photo_upload'),
    path('photos/gallery/', views.photo_gallery, name='photo_gallery'),
    path('api/locations/', views.locations_api, name='locations_api'),
    path('api/party-photos/', views.party_photos_api, name='party_photos_api'),
    path('api/photos/', views.photos_api, name='photos_api'),
    path('api/rsvp-names/', views.rsvp_names_api, name='rsvp_names_api'),
]
