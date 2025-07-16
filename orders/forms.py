from django import forms
from django.core.validators import RegexValidator


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Full Name',
            'required': True
        }),
        label='Full Name'
    )

    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'email@example.com',
            'required': True
        }),
        label='Email Address'
    )

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    customer_phone = forms.CharField(
        validators=[phone_validator],
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '+60 12-345 6789',
            'required': True
        }),
        label='Phone Number'
    )

    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full',
            'placeholder': 'Enter your full delivery address including postal code',
            'rows': 4,
            'required': True
        }),
        label='Delivery Address'
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full',
            'placeholder': 'Special instructions, dietary requirements, or other notes (optional)',
            'rows': 3
        }),
        label='Order Notes (Optional)'
    )

    def clean_customer_name(self):
        name = self.cleaned_data.get('customer_name')
        if name:
            name = name.strip()
            if len(name) < 2:
                raise forms.ValidationError('Please enter a valid full name.')
            return name
        return name

    def clean_delivery_address(self):
        address = self.cleaned_data.get('delivery_address')
        if address:
            address = address.strip()
            if len(address) < 10:
                raise forms.ValidationError('Please enter a complete delivery address.')
            return address
        return address
