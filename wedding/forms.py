from django import forms
from .models import RSVP


class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'attendance', 'number_of_guests', 'guest_names',
            'dietary_restrictions', 'song_request', 'message'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(123) 456-7890'
            }),
            'attendance': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            }),
            'guest_names': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Please list the names of additional guests'
            }),
            'dietary_restrictions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Any dietary restrictions or allergies we should know about?'
            }),
            'song_request': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What song would you love to hear at the reception?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Any message for the happy couple?'
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'attendance': 'Will you be attending?',
            'number_of_guests': 'Number of Guests',
            'guest_names': 'Guest Names',
            'dietary_restrictions': 'Dietary Restrictions',
            'song_request': 'Song Request',
            'message': 'Message to the Couple',
        }
