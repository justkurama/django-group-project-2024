from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_listing, name='create_listing'),
    path('success/', views.success_creation_lising, name='success_creation_listing'),
    path('', views.listing_list, name='listing_list'),
    path('own/', views.my_listings, name='my_listings'),
    path('<int:id>/', views.listing_detail, name='listing_detail'),
    path('<int:id>/update/', views.update_listing, name='listing_update'),
    path('<int:id>/delete/', views.delete_listing, name='listing_delete'),
    path('<int:id>/delete_image/', views.delete_image, name='delete_image'),



    path('<int:listing_id>/rooms/', views.room_list, name='room_list'),
    path('<int:listing_id>/rooms/create/',views.create_room, name='create_room'),
    path('<int:listing_id>/rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    # path('rooms/<int:id>/update/', views.update_room, name='room_update'),
    # path('rooms/<int:id>/delete/', views.delete_room, name='room_delete'),
]