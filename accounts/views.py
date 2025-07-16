from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('products:product_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')

            # Log the user in after registration
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)
                return redirect('products:product_list')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('products:product_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')

                # Redirect to next page or default
                next_page = request.GET.get('next')
                return redirect(next_page) if next_page else redirect('products:product_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('products:product_list')


@login_required
def profile_view(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'profile': profile,
        'user': request.user,
    }

    return render(request, 'accounts/profile.html', context)
