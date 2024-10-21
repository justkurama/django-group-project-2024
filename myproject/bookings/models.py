from django.db import models
from users.models import User
from listings.models import Listing, Room

# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_host': False})
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    paypal_transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Booking {self.id} - {self.customer.email} - {self.listing.title}" 
    
class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Payment {self.id} - {self.booking.id}"

class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} - {self.customer.email} - {self.listing.id}"