from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Listing, Room, ListingImage, RoomImage
from .forms import ListingCreationForm, RoomCreationForm, ListingImageFormSet, RoomImageFormSet
from django.contrib import messages


# Create your views here.

def create_listing(request):
    if request.method == 'POST':
        form = ListingCreationForm(request.POST, request.FILES)
        imageset = ListingImageFormSet(request.POST, request.FILES, queryset=ListingImage.objects.none())
        if form.is_valid() and imageset.is_valid():
            listing = form.save(commit=False)
            listing.host = request.user
            listing.save() 
            for image in imageset.cleaned_data:
                if image:
                    picture = image['image']
                    ListingImage.objects.create(listing=listing, image=picture)

            messages.success(request, 'Listing created Succesfully')
            # TODO: redirect to the listing_detail page 
            return redirect('success_creation')
        else: 
            messages.error(request, 'Listing isn\'t created!!!')
    else:
        form = ListingCreationForm()
        imageset = ListingImageFormSet()
    
    return render(request, 'listing/create.html', {'form': form,
                                                   'formset': imageset})

def success_creation(request):
    return render(request, 'listing/success.html')

def listing_list(request):
    listings = Listing.objects.all()
    template = loader.get_template('listing/list.html')
    context ={
        'listings': listings,
    }

    return HttpResponse(template.render(request=request, context=context))

def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)
    template = loader.get_template('listing/detail.html')
    context ={
        'listing': listing,
        'user': request.user,
    }

    return HttpResponse(template.render(request=request, context=context))


def update_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.method == 'POST':
        form = ListingCreationForm(request.POST, instance=listing)
        images = ListingImageFormSet(request.POST, request.FILES, queryset=ListingImage.objects.filter(listing = listing))

        if form.is_valid() and images.is_valid():
            form.save()
            for image in images.cleaned_data:
                if image:
                    picture = image['image']
                    ListingImage.objects.create(listing=listing, image=picture)
            return redirect('listing_detail', id=listing.id)
    else:
        form = ListingCreationForm(request.POST, instance=listing)
        images = ListingImageFormSet(request.POST, request.FILES, queryset=ListingImage.objects.filter(listing = listing))
    return render(request, 'listing/update.html', {'listing_form': form,
                                                    'formset': images})

def delete_listing(request, id):
    listing = Listing.objects.filter(id=id)
    if request.method == 'POST' and listing.host == request.user: 
        ListingImage.objects.filter(listing = listing).delete()
        listing.delete()
        return redirect('listing_list')
    return redirect('listing_deatil')

# All about room
def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST, request.FILES)
        imageset = RoomImageFormSet(request.POST, request.FILES, queryset=RoomImage.objects.none())
        if form.is_valid() and imageset.is_valid():
            room = form.save(commit=False)
            # FIXME: ???
            room.save() 
            for image in imageset.cleaned_data:
                if image:
                    picture = image['image']
                    RoomImage.objects.create(room=room, image=picture)

            messages.success(request, 'Listing created Succesfully')
            # TODO: redirect to the success page 
            return redirect('success_creation')
        else: 
            messages.error(request, 'Room isn\'t created!!!')
    else:
        form = RoomCreationForm()
        imageset = RoomImageFormSet()
    
    return render(request, 'room/create.html', {'form': form,
                                                   'formset': imageset})
               
def success_creation(request):
    return render(request, 'listing/success.html')

def room_list(request):
    rooms = Room.objects.all()
    template = loader.get_template('room/list.html')
    context ={
        'rooms': rooms,
    }

    return HttpResponse(template.render(context, request))

def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    template = loader.get_template('room/detail.html')
    context ={
        'room': room,
        'user': request.user,
    }

    return HttpResponse(template.render(context, request))


def update_room(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == 'POST':
        form = RoomCreationForm(request.POST, instance=room)
        images = RoomImageFormSet(request.POST, request.FILES, queryset=RoomImage.objects.filter(room = room))

        if form.is_valid() and images.is_valid():
            form.save()
            for image in images.cleaned_data:
                if image:
                    picture = image['image']
                    RoomImage.objects.create(room=room, image=picture)
            return redirect('room_detail', id=room.id)
    else:
        form = RoomCreationForm(request.POST, instance=room)
        images = RoomImageFormSet(request.POST, request.FILES, queryset=RoomImage.objects.filter(room = room))
    return render(request, 'room/update.html', {'room_form': form,
                                                    'formset': images})

def delete_room(request, room_id):
    room = Listing.objects.filter(id=room_id)
    if request.method == 'POST' and room.host == request.user: 
        RoomImage.objects.filter(room = room).delete()
        room.delete()
    return redirect('room_list')