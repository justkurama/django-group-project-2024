from django import forms
from .models import Booking, Payment, Review

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']

class PaymentForm(forms.ModelForm):
    pass


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']