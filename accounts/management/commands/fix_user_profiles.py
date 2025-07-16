from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Fixes user profile issues by creating missing profiles and checking integrity'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating profiles',
        )
        parser.add_argument(
            '--check-only',
            action='store_true',
            help='Only check for issues without creating profiles',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        check_only = options['check_only']

        self.stdout.write(self.style.HTTP_INFO('Checking user profiles...'))

        # Get all users and profile statistics
        all_users = User.objects.all()
        all_profiles = UserProfile.objects.all()
        users_without_profiles = User.objects.filter(userprofile__isnull=True)

        # Display statistics
        self.stdout.write('User Profile Statistics:')
        self.stdout.write('  Total users: {}'.format(all_users.count()))
        self.stdout.write('  Total profiles: {}'.format(all_profiles.count()))
        self.stdout.write('  Users without profiles: {}'.format(users_without_profiles.count()))

        if not users_without_profiles.exists():
            self.stdout.write(self.style.SUCCESS('All users already have profiles!'))
            return

        # Show users without profiles
        self.stdout.write(self.style.WARNING('Users missing profiles:'))
        for user in users_without_profiles:
            user_info = '  - {} (ID: {})'.format(user.username, user.id)
            if user.email:
                user_info += ' Email: {}'.format(user.email)
            self.stdout.write(user_info)

        if check_only:
            self.stdout.write(self.style.HTTP_INFO('Check complete. Use --dry-run or run without flags to fix.'))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN: Would create {} profiles'.format(users_without_profiles.count())))
            return

        # Create missing profiles
        self.stdout.write(self.style.HTTP_INFO('Creating missing profiles...'))
        created_count = 0
        error_count = 0

        for user in users_without_profiles:
            try:
                profile = UserProfile.objects.create(user=user)
                created_count += 1
                self.stdout.write('  Created profile for: {}'.format(user.username))
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR('  Failed to create profile for {}: {}'.format(user.username, str(e)))
                )

        # Final summary
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully created {} user profiles!'.format(created_count))
            )

        if error_count > 0:
            self.stdout.write(
                self.style.ERROR('Failed to create {} profiles. Check errors above.'.format(error_count))
            )

        # Verify final state
        remaining_without_profiles = User.objects.filter(userprofile__isnull=True).count()
        if remaining_without_profiles == 0:
            self.stdout.write(self.style.SUCCESS('All users now have profiles!'))
        else:
            self.stdout.write(
                self.style.WARNING('{} users still without profiles'.format(remaining_without_profiles))
            )
