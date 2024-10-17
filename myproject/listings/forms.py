from .models import Listing, Room, ListingImage, RoomImage
from django import forms
from django.forms import modelformset_factory


class ListingCreationForm(forms.ModelForm):
    class Meta:
        model = Listing
        # fields = ['available_from', ]
        exclude = ['created_at', ]
        

ListingImageFormSet = modelformset_factory(ListingImage, fields=('image',), extra=6)

RoomImageFormSet = modelformset_factory(RoomImage, fields=('image',), extra=6)

class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['created_at', ]