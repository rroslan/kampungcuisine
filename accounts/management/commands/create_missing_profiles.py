from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Creates missing UserProfile objects for existing users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating profiles'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Find users without profiles
        users_without_profiles = User.objects.filter(userprofile__isnull=True)

        if not users_without_profiles.exists():
            self.stdout.write(
                self.style.SUCCESS('All users already have profiles!')
            )
            return

        count = users_without_profiles.count()

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    'DRY RUN: Would create {} missing user profiles:'.format(count)
                )
            )
            for user in users_without_profiles:
                self.stdout.write('  - {} (ID: {})'.format(user.username, user.id))
            return

        # Create missing profiles
        created_count = 0
        for user in users_without_profiles:
            try:
                UserProfile.objects.create(user=user)
                created_count += 1
                self.stdout.write('Created profile for user: {}'.format(user.username))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        'Failed to create profile for user {}: {}'.format(user.username, str(e))
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created {} user profiles!'.format(created_count)
            )
        )
