#!/usr/bin/env python
"""
Check User Profiles Script
This script verifies that all users have corresponding UserProfile objects.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile


def check_user_profiles():
    """Check if all users have corresponding profiles."""
    print("🔍 Checking User Profiles...")
    print("=" * 50)

    # Get all users
    all_users = User.objects.all()
    users_with_profiles = User.objects.filter(userprofile__isnull=False)
    users_without_profiles = User.objects.filter(userprofile__isnull=True)

    print(f"📊 User Statistics:")
    print(f"  Total users: {all_users.count()}")
    print(f"  Users with profiles: {users_with_profiles.count()}")
    print(f"  Users without profiles: {users_without_profiles.count()}")
    print()

    if users_without_profiles.exists():
        print("❌ Users missing profiles:")
        for user in users_without_profiles:
            print(f"  - {user.username} (ID: {user.id}, Email: {user.email})")
        print()
        print("🔧 To fix this, run:")
        print("  python manage.py create_missing_profiles")
        return False
    else:
        print("✅ All users have profiles!")
        print()
        print("👥 User Details:")
        for user in all_users:
            profile = user.userprofile
            print(f"  - {user.username}")
            print(f"    Email: {user.email}")
            print(f"    Profile ID: {profile.id}")
            print(f"    Phone: {profile.phone_number or 'Not set'}")
            print(f"    Created: {profile.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()
        return True


def check_profile_integrity():
    """Check for orphaned profiles or other integrity issues."""
    print("🔍 Checking Profile Integrity...")
    print("=" * 50)

    # Check for orphaned profiles (profiles without users)
    orphaned_profiles = UserProfile.objects.filter(user__isnull=True)

    if orphaned_profiles.exists():
        print(f"⚠️  Found {orphaned_profiles.count()} orphaned profiles:")
        for profile in orphaned_profiles:
            print(f"  - Profile ID: {profile.id}")
        print("Consider cleaning these up manually.")
    else:
        print("✅ No orphaned profiles found!")

    print()


def main():
    """Main function to run all checks."""
    try:
        print("🏥 User Profile Health Check")
        print("=" * 50)
        print()

        profiles_ok = check_user_profiles()
        check_profile_integrity()

        if profiles_ok:
            print("🎉 All user profile checks passed!")
            sys.exit(0)
        else:
            print("⚠️  Some issues found. Please fix them before proceeding.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error during check: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
