from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from .forms import CombinedProfileForm


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


@login_required
def edit_profile_view(request):
    """Edit user profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        combined_form = CombinedProfileForm(
            user_instance=request.user,
            profile_instance=profile,
            data=request.POST
        )

        if combined_form.is_valid():
            user, profile = combined_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
        else:
            # If there are errors, they will be displayed in the template
            messages.error(request, 'Please correct the errors below.')
    else:
        combined_form = CombinedProfileForm(
            user_instance=request.user,
            profile_instance=profile
        )

    context = {
        'user_form': combined_form.user_form,
        'profile_form': combined_form.profile_form,
        'profile': profile,
    }

    return render(request, 'accounts/edit_profile.html', context)
