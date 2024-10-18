from django.urls import path, include
from . import views
urlpatterns = [
    path('create/<int:listing_id>/<int:room_id>/', views.booking_create, name="booking_create"),
    path('<int:booking_id>/', views.booking_detail, name="booking_detail"),
    path('list/', views.booking_list, name="booking_list"),
    path('payments/<int:booking_id>/create/', views.payment_create, name="payment_create"),
    path('payments/<int:booking_id>/success/', views.payment_success, name="payment_success"),
    path('payments/<int:booking_id>/cancel/', views.payment_cancel, name="payment_cancel"),
]