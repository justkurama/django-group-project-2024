from .models import Listing, Room, ListingImage, RoomImage
from django import forms



class ListingCreationForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'property_type',
            'address',
            'city',
            'country',
            'price_per_night',
            'available_from',
            'available_to'
        ]
        


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'room_number',
            'description',
            'price_per_night',
            'capacity',
            'available_from',
            'available_to',
        ]