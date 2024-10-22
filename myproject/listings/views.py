from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Listing, Room, ListingImage, RoomImage
from .forms import ListingCreationForm, RoomCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def create_listing(request):
    if not request.user.is_host:
        messages.error(request, 'You do not have permission to create a listing.')
        return redirect('listing_list')

    if request.method == 'POST':
        form = ListingCreationForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            listing = form.save(commit=False)
            listing.host = request.user
            listing.save() 

            if images:  
                for image in images:
                    ListingImage.objects.create(listing=listing, image=image)

            messages.success(request, 'Listing created successfully')
            return redirect('success_creation_listing')
        else: 
            messages.error(request, 'Listing isn\'t created!!!')
    else:
        form = ListingCreationForm()
    
    return render(request, 'listing/create.html', {'form': form})

def success_creation_lising(request):
    return render(request, 'listing/success.html')

def listing_list(request):
    listings = Listing.objects.all()
    template = loader.get_template('listing/list.html')
    context = {
        'listings': listings,
    }

    return HttpResponse(template.render(request=request, context=context))

def my_listings(request):
    listings = Listing.objects.filter(host = request.user)
    template = loader.get_template('listing/list.html')
    context = {
        'listings': listings,
    }

    return HttpResponse(template.render(request=request, context=context))

def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)
    template = loader.get_template('listing/detail.html')
    context = {
        'listing': listing,
        'user': request.user,
    }

    return HttpResponse(template.render(request=request, context=context))

def update_listing(request, id):
    listing = get_object_or_404(Listing, id=id)

    if request.user != listing.host:
        messages.error(request, 'You do not have permission to update this listing.')
        return redirect('listing_detail', id=listing.id)

    
    if request.method == 'POST':
        form = ListingCreationForm(request.POST, request.FILES, instance=listing)  
        new_images = request.FILES.getlist('images')
        if form.is_valid():
            listing=form.save()

            if new_images:  
                for image in new_images:
                    ListingImage.objects.create(listing=listing, image=image)
            
            return redirect('listing_detail', id=listing.id)
    else:
        form = ListingCreationForm(request.POST, request.FILES, instance=listing)

    existing_images = listing.images.all()  # Assuming related_name='images' in ListingImage

    return render(request, 'listing/update.html', {
        'form': form,
        'listing': listing,
        'existing_images': existing_images,})

def delete_image(request, id):
    image = get_object_or_404(ListingImage, id=id)
    # Check if the user has permission to delete this image
    if request.user == image.listing.host:
        image.delete()
        messages.success(request, 'Image deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this image.')
    
    return redirect('listing_update', id=image.listing.id)

def delete_listing(request, id):
    listing = get_object_or_404(Listing, id=id)

    if request.user != listing.host:
        messages.error(request, 'You do not have permission to delete this listing.')
        return redirect('listing_detail', id=listing.id)

    listing.delete()
    messages.success(request, 'Listing deleted successfully.')
    return redirect('listing_list')

    

# All about room
def create_room(request, listing_id):
    listing = get_list_or_404(Listing, id=listing_id)
    if not request.user.is_host:
        messages.error(request, 'You do not have permission to create a room.')
        return redirect('listing_list')

    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = listing
            room.save() 

            if images:  
                for image in images:
                    RoomImage.objects.create(room=room, image=image)

            messages.success(request, 'Room created successfully')
            return redirect('success_creation_room')
        else: 
            messages.error(request, 'Room isn\'t created!!!')
    else:
        form = RoomCreationForm()
    
    return render(request, 'room/create.html', {'form_room': form})


def success_creation_room(request):
    return render(request, 'room/success.html')

def room_list(request):
    rooms = Room.objects.all()
    template = loader.get_template('room/list.html')
    context = {
        'rooms': rooms,
    }

    return HttpResponse(template.render(context, request))

def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    template = loader.get_template('room/detail.html')
    context = {
        'room': room,
        'user': request.user,
    }

    return HttpResponse(template.render(context, request))

# def update_room(request, id):
#     room = get_object_or_404(Room, id=id)
#     if request.method == 'POST':
#         form = RoomCreationForm(request.POST, instance=room)
        

#         if form.is_valid() and images.is_valid():
#             form.save()
#             for image in images.cleaned_data:
#                 if image:
#                     picture = image['image']
#                     RoomImage.objects.create(room=room, image=picture)
#             return redirect('room_detail', id=room.id)
#     else:
#         form = RoomCreationForm(request.POST, instance=room)
        
#     return render(request, 'room/update.html', {'room_form': form})

# def delete_room(request, room_id):
#     room = Listing.objects.filter(id=room_id)
#     if request.method == 'POST' and room.host == request.user: 
#         RoomImage.objects.filter(room=room).delete()
#         room.delete()
#     return redirect('room_list')
