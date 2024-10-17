from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from models import Listing, Room, ListingImage, RoomImage
from forms import ListingCreationForm, RoomCreationForm, ListingImageFormSet, RoomImageFormSet
from django.contrib import messages


# Create your views here.

def create_listing(request):
    if request.method == 'POST':
        form = ListingCreationForm(request.POST. request.FILES)
        imageset = ListingImageFormSet(request.POST, request.FILES, queryset=ListingImage.objects.none())
        if form.is_valid() and imageset.is_valid():
            listing = form.save(commit=False)
            listing.host = request.user
            listing.save() 
            for image in imageset:
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

    return HttpResponse(template.render(request, context))

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    template = loader.get_template('listing/detail.html')
    context ={
        'listing': listing,
        'user': request.user,
    }

    return HttpResponse(template.render(request, context))


def update_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = ListingCreationForm(request.POST, instance=listing_detail)
        images = ListingImageFormSet(request.POST, request.FILES, queryset=ListingImage.objects.filter(listing = listing))

        if form.is_valid() and images.is_valid():
            form.save()
            for image in images.cleaned_data:
                if image:
                    picture = image['image']
                    ListingImage.objects.create(listing=listing, image=picture)
            return redirect('listing_detail', id=listing.id)
    else:
        form = ListingCreationForm(request.POST, instance=listing_detail)
        images = ListingImageFormSet(request.POST, request.FILES, queryset=ListingImage.objects.filter(listing = listing))
    return render(request, 'listing/update.html', {'listing_form': form,
                                                    'formset': images})

def delete_listing(request, listing_id):
    listing = Listing.objects.filter(id=listing_id)
    if request.method == 'POST' and listing.host == request.user: 
        ListingImage.objects.filter(listing = listing).delete()
        listing.delete()
        return redirect('listing_list')
    return redirect('listing_deatil')

# 
def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST. request.FILES)
        imageset = RoomImageFormSet(request.POST, request.FILES, queryset=RoomImage.objects.none())
        if form.is_valid() and imageset.is_valid():
            room = form.save(commit=False)
            # FIXME:
            room.hotel = request.user.hotel
            room.save() 
            for image in imageset:
                if image:
                    picture = image['image']
                    RoomImage.objects.create(room=room, image=picture)

            messages.success(request, 'Listing created Succesfully')
            # TODO: redirect to the listing_detail page 
            return redirect('success_creation')
        else: 
            messages.error(request, 'Room isn\'t created!!!')
    else:
        form = RoomCreationForm()
        imageset = RoomImageFormSet()
    
    return render(request, 'room/create.html', {'form': form,
                                                   'formset': imageset})
               