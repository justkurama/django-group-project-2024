from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import create_listing, success_creation, listing_list, listing_detail, update_listing, delete_listing
from .views import create_room, room_list, room_detail, update_room, delete_room

urlpatterns = [
    path('create/', create_listing, name='create_listing'),
    path('success/', success_creation, name='success_creation'),
    path('', listing_list, name='listing_list'),
    path('<int:id>/', listing_detail, name='listing_detail'),
    path('<int:id>/update/', update_listing, name='listing_update'),
    path('<int:id>/delete/', delete_listing, name='listing_delete'),
    path('rooms/', room_list, name='room_list'),
    path('create_room/', create_room, name='create_room'),
    path('rooms/<int:id>/', room_detail, name='room_detail'),
    path('rooms/<int:id>/update/', update_room, name='room_update'),
    path('rooms/<int:id>/delete/', delete_room, name='room_delete'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)