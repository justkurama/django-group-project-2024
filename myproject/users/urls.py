from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('update/', views.update_user, name='update'),
    path('delete/', views.delete_user, name='delete'),
    path('profile/', views.profile, name='profile'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('password/', views.change_password, name='password_reset'),
]