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
    path('api/locations/', views.locations_api, name='locations_api'),
    path('api/party-photos/', views.party_photos_api, name='party_photos_api'),
]
