from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from .models import User, Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'users/register.html', {'form': form, 'profile_form': profile_form})

def login_user(request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'users/login.html', {'error': 'Invalid email or password'})
        return render(request, 'users/login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request, 'users/change_password.html', {'form': form, 'message': 'Password has been changed successfully'})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def update_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('profile')
        if 'cancel' in request.POST:
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/update.html', {'form': form, 'profile_form': profile_form})
    
@login_required
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    return render(request, 'users/delete.html', {'user': user})

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_detail.html', {'user': user})

