from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from .forms import BookingForm, PaymentForm, ReviewForm
from .models import Booking, Payment, Review
from listings.models import Listing, Room

def booking_create(request, listing_id, room_id):
    listing = get_object_or_404(Listing, id=listing_id)
    room = None
    if room_id:
        room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.listing = listing
            if room:
                booking.room = room
            
            booking.total_price = calc_total_price(booking.check_in, booking.check_out, listing, room)
            booking.save()
            return redirect('payment_create', booking_id=booking.id)
        
    else:
        form = BookingForm()

    template = loader.get_template('bookings/booking_create.html')
    context = {
        'listing': listing,
        'room': room,
        'form': form,
    }

    return HttpResponse(template.render(context=context, request=request))
    

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    template = loader.get_template('bookings/booking_detail.html')
    context = {
        'booking': booking
    }

    return HttpResponse(template.render(context=context, request=request))



def booking_list(request):
    bookings = Booking.objects.filter(customer=request.user)
    template = loader.get_template('bookings/booking_list.html')
    context = {
        'bookings': bookings,
    }

    return HttpResponse(template.render(context=context, request=request))


def payment_create(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    payment = Payment.objects.create(booking=booking, amount=booking.total_price)

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(payment.amount),
        'item_name': f"Booking #{booking.id}",
        'invoice': str(payment.id),
        'currency_code': 'USD',
        'charset': 'UTF-8',
        'notify_url':  request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payment_success', kwargs={'booking_id': booking.id, 'payment_id': payment.id})),
        'cancel_url':  request.build_absolute_uri(reverse('payment_cancel', kwargs={'booking_id': booking.id})),
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'booking': booking,
        'payment': payment,
        'paypal': paypal_payment,
    }

    return HttpResponse(loader.get_template('bookings/payment_create.html').render(context=context, request=request))

def payment_success(request, booking_id, payment_id):
    booking = Booking.objects.get(id=booking_id)
    payment = Payment.objects.get(id=payment_id)
    payment.status = "Paid"
    booking.status = "Confirmed"
    booking.save()
    payment.save()

    return HttpResponse(loader.get_template('bookings/payment_success.html').render(request=request, context={"booking": booking}))

def payment_cancel(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return HttpResponse(loader.get_template('bookings/payment_cancel.html').render(request=request, context={"booking": booking}))

def review_create(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.listing = listing
            review.save()
    
    else:
        form = ReviewForm()

    template = loader.get_template('review_create.html')
    context = {
        'listing': listing,
        'form': form,
    }

    return HttpResponse(template.render(context=context, request=request))


def review_list(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    reviews = Review.objects.filter(Review, listing=listing)
    template = loader.get_template('review_list.html')
    context = {
        'reviews': reviews,
    }

    return HttpResponse(template.render(context=context, request=request))


def review_update(request, booking_id, review_id):
    review = Review.objects.get(id=review_id)
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        form.save()
        return redirect('booking_detail', booking_id)


def review_delete(request, booking_id, review_id):
    review = Review.objects.get(id=review_id)
    if review.customer == request.user:
        review.delete()
    
    return redirect('booking_detail', booking_id)


def calc_total_price(check_in, check_out, listing, room):
    days = (check_out - check_in).days
    price = room.price_per_night if room else listing.price_per_night
    return days * price
