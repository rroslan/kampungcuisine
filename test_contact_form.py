#!/usr/bin/env python
"""
Contact Form Test Script
Tests the contact form submission flow to ensure messages don't persist.
"""

import os
import sys
import requests
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_dev')

def test_contact_form():
    """Test contact form submission"""
    base_url = "http://127.0.0.1:8000"

    print("🧪 Testing Contact Form Submission")
    print("=" * 50)

    # Create a session to maintain cookies
    session = requests.Session()

    try:
        # 1. Get the contact form page to obtain CSRF token
        print("📄 Getting contact form page...")
        contact_url = f"{base_url}/contact/"
        response = session.get(contact_url)

        if response.status_code != 200:
            print(f"❌ Failed to get contact page: {response.status_code}")
            return False

        # Extract CSRF token
        csrf_token = None
        for line in response.text.split('\n'):
            if 'csrfmiddlewaretoken' in line and 'value=' in line:
                csrf_token = line.split('value="')[1].split('"')[0]
                break

        if not csrf_token:
            print("❌ Could not find CSRF token")
            return False

        print(f"✅ Got CSRF token: {csrf_token[:8]}...")

        # 2. Submit the contact form
        print("📝 Submitting contact form...")
        form_data = {
            'csrfmiddlewaretoken': csrf_token,
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'subject': 'general',
            'message': 'This is a test message to verify the contact form works correctly.'
        }

        response = session.post(contact_url, data=form_data)

        # Should redirect to success page
        if response.status_code == 302:
            print(f"✅ Form submitted successfully, redirected to: {response.headers.get('Location')}")

            # Follow the redirect
            success_response = session.get(response.headers.get('Location'))
            if success_response.status_code == 200:
                print("✅ Success page loaded correctly")

                # Check if success page contains success message
                if "Message Sent Successfully" in success_response.text:
                    print("✅ Success page shows correct message")
                else:
                    print("⚠️  Success page doesn't show expected message")

            else:
                print(f"❌ Failed to load success page: {success_response.status_code}")
                return False

        else:
            print(f"❌ Form submission failed: {response.status_code}")
            print("Response content:", response.text[:500])
            return False

        # 3. Check if messages persist by visiting contact page again
        print("🔍 Checking for persistent messages...")
        response = session.get(contact_url)

        if response.status_code == 200:
            # Look for thank you message in the contact page
            if "Thank you for your message" in response.text:
                print("❌ PROBLEM: Thank you message is persisting!")
                return False
            else:
                print("✅ No persistent messages found")

        # 4. Test visiting other pages to ensure no messages appear
        print("🏠 Testing homepage for persistent messages...")
        home_response = session.get(f"{base_url}/")

        if home_response.status_code == 200:
            if "Thank you for your message" in home_response.text:
                print("❌ PROBLEM: Message appearing on homepage!")
                return False
            else:
                print("✅ Homepage clean of messages")

        print("\n🎉 All tests passed! Contact form works correctly without persistent messages.")
        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Django is running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_server_running():
    """Check if Django server is running"""
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main test function"""
    print("🚀 Kampung Cuisine Contact Form Test")
    print("=" * 40)

    # Check if server is running
    if not test_server_running():
        print("❌ Django server is not running!")
        print("💡 Start the server with: python manage.py runserver --settings=core.settings_dev")
        return

    print("✅ Django server is running")
    print()

    # Run the test
    success = test_contact_form()

    print("\n" + "=" * 50)
    if success:
        print("✅ ALL TESTS PASSED")
        print("Contact form is working correctly without persistent messages!")
    else:
        print("❌ TESTS FAILED")
        print("There are issues with the contact form that need to be fixed.")

if __name__ == '__main__':
    main()
