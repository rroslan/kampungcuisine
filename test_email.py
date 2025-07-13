#!/usr/bin/env python
"""
Email Configuration Test Script for Kampungcuisine
This script helps test and diagnose email configuration issues.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_dev')
django.setup()

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.test import override_settings

def print_colored(message, color_code="0"):
    """Print colored message to terminal"""
    print(f"\033[{color_code}m{message}\033[0m")

def print_banner():
    """Print test banner"""
    print_colored("=" * 60, "96")  # Cyan
    print_colored("📧 KAMPUNGCUISINE EMAIL TEST UTILITY 📧", "93")  # Yellow
    print_colored("=" * 60, "96")  # Cyan
    print()

def show_current_config():
    """Display current email configuration"""
    print_colored("🔧 Current Email Configuration:", "94")  # Blue
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")

    if hasattr(settings, 'EMAIL_HOST'):
        print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    if hasattr(settings, 'EMAIL_PORT'):
        print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    if hasattr(settings, 'EMAIL_USE_TLS'):
        print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    if hasattr(settings, 'EMAIL_HOST_USER'):
        print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    if hasattr(settings, 'EMAIL_HOST_PASSWORD'):
        password_status = "SET" if settings.EMAIL_HOST_PASSWORD else "NOT SET"
        print(f"   EMAIL_HOST_PASSWORD: {password_status}")
    if hasattr(settings, 'DEFAULT_FROM_EMAIL'):
        print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

    print()

def check_environment():
    """Check environment variables"""
    print_colored("🔍 Environment Variables:", "94")  # Blue

    resend_key = os.getenv('RESEND_API_KEY')
    if resend_key:
        print_colored(f"   ✅ RESEND_API_KEY: SET (length: {len(resend_key)})", "92")  # Green
    else:
        print_colored("   ❌ RESEND_API_KEY: NOT SET", "91")  # Red

    use_real_email = os.getenv('USE_REAL_EMAIL', 'false')
    print(f"   USE_REAL_EMAIL: {use_real_email}")

    django_settings = os.getenv('DJANGO_SETTINGS_MODULE', 'NOT SET')
    print(f"   DJANGO_SETTINGS_MODULE: {django_settings}")

    print()

def test_console_email():
    """Test console email backend"""
    print_colored("📝 Testing Console Email Backend...", "94")  # Blue

    try:
        with override_settings(EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'):
            result = send_mail(
                subject='Test Email from Kampungcuisine',
                message='This is a test email to verify console backend works.',
                from_email='test@kampungcuisine.com',
                recipient_list=['test@example.com'],
                fail_silently=False
            )

        if result:
            print_colored("   ✅ Console email test passed", "92")  # Green
        else:
            print_colored("   ❌ Console email test failed", "91")  # Red

    except Exception as e:
        print_colored(f"   ❌ Console email test error: {e}", "91")  # Red

    print()

def test_smtp_email():
    """Test SMTP email backend with Resend"""
    print_colored("📧 Testing SMTP Email Backend...", "94")  # Blue

    resend_key = os.getenv('RESEND_API_KEY')
    if not resend_key:
        print_colored("   ❌ Cannot test SMTP: RESEND_API_KEY not set", "91")  # Red
        print_colored("   💡 Set your Resend API key: export RESEND_API_KEY=your_key_here", "93")  # Yellow
        return

    # Test SMTP settings
    smtp_settings = {
        'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'EMAIL_HOST': 'smtp.resend.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True,
        'EMAIL_USE_SSL': False,
        'EMAIL_HOST_USER': 'resend',
        'EMAIL_HOST_PASSWORD': resend_key,
        'DEFAULT_FROM_EMAIL': 'noreply@applikasi.tech',
    }

    print(f"   Host: {smtp_settings['EMAIL_HOST']}:{smtp_settings['EMAIL_PORT']}")
    print(f"   From: {smtp_settings['DEFAULT_FROM_EMAIL']}")

    try:
        with override_settings(**smtp_settings):
            email = EmailMessage(
                subject='Test Email from Kampungcuisine',
                body='''
Hello!

This is a test email sent from the Kampungcuisine application.

If you receive this email, it means the email configuration is working correctly.

Best regards,
Kampungcuisine Team
                '''.strip(),
                from_email=smtp_settings['DEFAULT_FROM_EMAIL'],
                to=['rroslan@gmail.com'],  # Send to the recipient from your contact form
                reply_to=['test@example.com']
            )

            result = email.send(fail_silently=False)

            if result:
                print_colored("   ✅ SMTP email test passed - Email sent successfully!", "92")  # Green
                print_colored("   📧 Check rroslan@gmail.com for the test email", "93")  # Yellow
            else:
                print_colored("   ❌ SMTP email test failed - No email sent", "91")  # Red

    except Exception as e:
        print_colored(f"   ❌ SMTP email test error: {e}", "91")  # Red

        # Provide specific error guidance
        error_str = str(e).lower()
        if 'authentication' in error_str:
            print_colored("   💡 This looks like an authentication error", "93")  # Yellow
            print_colored("   💡 Check your RESEND_API_KEY is correct", "93")  # Yellow
        elif 'connection' in error_str:
            print_colored("   💡 This looks like a connection error", "93")  # Yellow
            print_colored("   💡 Check your internet connection and firewall", "93")  # Yellow

    print()

def test_contact_form():
    """Test the actual contact form"""
    print_colored("📞 Testing Contact Form...", "94")  # Blue

    try:
        from pages.forms import ContactForm

        # Create a test contact form submission
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'subject': 'general',
            'message': 'This is a test message from the email test utility.'
        }

        form = ContactForm(data=form_data)

        if form.is_valid():
            result = form.send_email()
            if result:
                print_colored("   ✅ Contact form test passed", "92")  # Green
            else:
                print_colored("   ❌ Contact form test failed", "91")  # Red
        else:
            print_colored(f"   ❌ Contact form validation failed: {form.errors}", "91")  # Red

    except Exception as e:
        print_colored(f"   ❌ Contact form test error: {e}", "91")  # Red

    print()

def main():
    """Main test function"""
    print_banner()

    # Show current configuration
    show_current_config()

    # Check environment
    check_environment()

    # Test console email (should always work)
    test_console_email()

    # Ask user what they want to test
    print_colored("🤔 What would you like to test?", "95")  # Magenta
    print("   1. Test SMTP email (requires RESEND_API_KEY)")
    print("   2. Test contact form")
    print("   3. Both")
    print("   4. Exit")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == '1':
        test_smtp_email()
    elif choice == '2':
        test_contact_form()
    elif choice == '3':
        test_smtp_email()
        test_contact_form()
    elif choice == '4':
        print_colored("👋 Goodbye!", "93")  # Yellow
        return
    else:
        print_colored("❌ Invalid choice", "91")  # Red
        return

    print_colored("✅ Email testing complete!", "92")  # Green
    print()
    print_colored("💡 Next steps:", "93")  # Yellow
    print("   1. If SMTP test failed, check your RESEND_API_KEY")
    print("   2. To enable real emails in development: export USE_REAL_EMAIL=true")
    print("   3. To test in browser: python manage.py runserver --settings=core.settings_dev")

if __name__ == '__main__':
    main()
