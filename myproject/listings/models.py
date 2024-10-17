from django.db import models
from users.models import User

# Create your models here.
class Listing(models.Model):
    PROPERTY_TYPES = [
        ('Hotel', 'Hotel'),
        ('Apartment', 'Apartment'),
        ('House', 'House')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(choices=PROPERTY_TYPES, default='Hotel')
    address = models.CharField(max_length=255)    
    city = models.CharField(max_length=255)    
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    price_per_night = models.FloatField()
    available_from = models.DateField()
    available_from = models.DateField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, name='users_listings') 


    def __str__(self) -> str:
        return f"{self.title} - {self.price_per_night} - {self.property_type}"

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.listing.title}"
    

class Room(models.Model):
    room_number = models.IntegerField(max_length=3)
    description = models.TextField()
    price_per_night = models.FloatField()
    capacity = models.IntegerField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    hotel = models.ForeignKey(Listing, on_delete=models.CASCADE, name='hotel_rooms')
    available_from = models.DateField()
    available_from = models.DateField()

    def __str__(self) -> str:
        return f"{self.room_number}: {self.price_per_night}"
    
class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.listing.title}"
