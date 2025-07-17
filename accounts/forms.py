from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information"""

    class Meta:
        model = UserProfile
        fields = ['address', 'phone']
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3,
                'placeholder': 'Enter your full address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '+60 12-345-6789',
                'maxlength': '20'
            })
        }
        help_texts = {
            'address': 'Your delivery address',
            'phone': 'Optional phone number for order updates'
        }


class UserForm(forms.ModelForm):
    """Form for editing basic user information"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter your email address'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email is already taken by another user
            existing_user = User.objects.filter(email=email).exclude(pk=self.instance.pk)
            if existing_user.exists():
                raise forms.ValidationError("This email address is already in use.")
        return email


class CombinedProfileForm:
    """Combined form handler for user and profile forms"""

    def __init__(self, user_instance, profile_instance, data=None):
        self.user_form = UserForm(data=data, instance=user_instance)
        self.profile_form = UserProfileForm(data=data, instance=profile_instance)

    def is_valid(self):
        return self.user_form.is_valid() and self.profile_form.is_valid()

    def save(self):
        if self.is_valid():
            user = self.user_form.save()
            profile = self.profile_form.save()
            return user, profile
        return None, None

    @property
    def errors(self):
        errors = {}
        errors.update(self.user_form.errors)
        errors.update(self.profile_form.errors)
        return errors
