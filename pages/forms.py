from django import forms
from django.core.mail import EmailMessage
from django.conf import settings


class ContactForm(forms.Form):
    """Contact form for customer inquiries"""

    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('product', 'Product Question'),
        ('order', 'Order Support'),
        ('returns', 'Returns & Exchanges'),
        ('wholesale', 'Wholesale Inquiry'),
        ('technical', 'Technical Support'),
        ('other', 'Other'),
    ]

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Your full name'
        }),
        help_text='Enter your full name'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'your.email@example.com'
        }),
        help_text='We will respond to this email address'
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '+1 (555) 123-4567'
        }),
        help_text='Optional: Phone number for urgent matters'
    )

    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full',
            'rows': 6,
            'placeholder': 'Please describe your inquiry in detail...'
        }),
        min_length=10,
        max_length=2000
    )

    def clean_message(self):
        """Validate message length and content"""
        message = self.cleaned_data.get('message')
        if message:
            if len(message.strip()) < 10:
                raise forms.ValidationError('Please provide a more detailed message (at least 10 characters).')

            # Basic spam detection
            spam_words = ['free money', 'click here now', 'limited time', 'act now']
            message_lower = message.lower()
            for spam_word in spam_words:
                if spam_word in message_lower:
                    raise forms.ValidationError('Your message appears to contain spam content. Please revise.')

        return message

    def clean_phone(self):
        """Clean and validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common phone number formatting
            import re
            phone = re.sub(r'[^\d+]', '', phone)
            if phone and len(phone) < 7:
                raise forms.ValidationError('Please enter a valid phone number.')
        return phone

    def send_email(self):
        """Send contact form email using the existing email configuration"""
        if not self.is_valid():
            return False

        try:
            # Prepare email content
            name = self.cleaned_data['name']
            email = self.cleaned_data['email']
            phone = self.cleaned_data.get('phone', '')
            subject_choice = self.cleaned_data['subject']
            message = self.cleaned_data['message']

            # Get subject display name
            subject_display = dict(self.SUBJECT_CHOICES).get(subject_choice, 'General Inquiry')

            # Email subject
            email_subject = f'Contact Form: {subject_display} - {name}'

            # Email body - conditionally include phone if provided
            phone_info = f"- Phone: {phone}\n" if phone.strip() else ""

            email_body = f"""
New contact form submission from Kampung Cuisine website:

Contact Information:
- Name: {name}
- Email: {email}
{phone_info}- Subject: {subject_display}

Message:
{message}

---
This message was sent from the Kampung Cuisine contact form.
Reply directly to this email to respond to the customer.
            """.strip()

            # Send email using Django's EmailMessage (configured with Resend)
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['rroslan@gmail.com'],  # Send to recipient email
                reply_to=[email],  # Allow direct reply to customer
            )

            result = email_message.send(fail_silently=False)
            return result

        except Exception as e:
            # Log the error with more details
            import traceback
            error_details = traceback.format_exc()
            print(f"Failed to send contact email: {str(e)}")
            print(f"Error details: {error_details}")
            print(f"Email config - HOST: {settings.EMAIL_HOST}, PORT: {settings.EMAIL_PORT}")
            print(f"From email: {settings.DEFAULT_FROM_EMAIL}")
            print(f"Recipient: rroslan@gmail.com")
            return False


class NewsletterSignupForm(forms.Form):
    """Simple newsletter signup form for footer/sidebar"""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your email'
        }),
        help_text='Subscribe to get updates on new products and special offers'
    )

    def clean_email(self):
        """Validate email and check for duplicates if needed"""
        email = self.cleaned_data.get('email')
        if email:
            # Basic email validation (Django already handles format)
            # You could add duplicate checking here if you store subscribers
            pass
        return email
