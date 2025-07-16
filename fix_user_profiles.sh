#!/bin/bash

# Fix User Profiles Script
# This script fixes common user profile issues in the Django project

echo "🔧 Fixing User Profile Issues..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: This script must be run from the Django project root directory"
    echo "   (where manage.py is located)"
    exit 1
fi

# Check if Django is properly set up
echo "🔍 Checking Django setup..."
python manage.py check --quiet
if [ $? -ne 0 ]; then
    echo "❌ Django configuration has issues. Please fix them first."
    exit 1
fi

echo "✅ Django setup is OK"

# Run migrations to ensure all models are up to date
echo "🔄 Running migrations..."
python manage.py migrate --verbosity=1

if [ $? -ne 0 ]; then
    echo "❌ Migration failed. Please check for migration errors."
    exit 1
fi

echo "✅ Migrations completed successfully"

# Check current user profile status
echo "📊 Checking current user profile status..."
python check_user_profiles.py --quiet 2>/dev/null
profile_check_result=$?

if [ $profile_check_result -eq 0 ]; then
    echo "✅ All users already have profiles!"
else
    echo "⚠️  Some users are missing profiles. Creating them..."

    # Create missing profiles
    python manage.py create_missing_profiles

    if [ $? -eq 0 ]; then
        echo "✅ Missing profiles created successfully"
    else
        echo "❌ Failed to create missing profiles"
        exit 1
    fi
fi

# Final verification
echo "🔍 Final verification..."
python check_user_profiles.py --quiet 2>/dev/null

if [ $? -eq 0 ]; then
    echo "🎉 All user profile issues have been resolved!"
    echo ""
    echo "💡 Summary of fixes applied:"
    echo "   ✓ Updated user profile signal to handle existing users"
    echo "   ✓ Created missing UserProfile objects"
    echo "   ✓ Verified profile integrity"
    echo ""
    echo "🔐 You should now be able to log into the admin panel"
    echo "🌐 Try accessing: http://localhost:8000/admin/"
else
    echo "❌ Some issues remain. Please check the output above."
    exit 1
fi

# Optional: Show user statistics
echo ""
echo "📈 Current User Statistics:"
python -c "
import os, sys, django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from django.contrib.auth.models import User
from accounts.models import UserProfile
users = User.objects.all()
profiles = UserProfile.objects.all()
print(f'   Total users: {users.count()}')
print(f'   Total profiles: {profiles.count()}')
print('   Users:')
for user in users:
    print(f'     - {user.username} ({user.email or \"no email\"})')
"

echo ""
echo "✅ User profile fix completed successfully!"
