from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.contrib.messages import get_messages
from django.contrib.messages.storage import default_storage
from django.http import HttpRequest


class Command(BaseCommand):
    help = 'Clear all persistent messages from sessions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all-sessions',
            action='store_true',
            help='Clear all sessions (will log out all users)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']

        if options['all_sessions']:
            # Clear all sessions
            session_count = Session.objects.count()
            Session.objects.all().delete()

            if verbose:
                self.stdout.write(
                    self.style.SUCCESS(f'Cleared {session_count} sessions')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('All sessions cleared')
                )
        else:
            # Clear messages from existing sessions
            cleared_count = 0
            total_sessions = Session.objects.count()

            for session in Session.objects.all():
                session_data = session.get_decoded()

                # Check if session has messages
                if '_messages' in session_data:
                    # Remove messages from session data
                    del session_data['_messages']

                    # Save the updated session
                    session.session_data = session.encode(session_data)
                    session.save()
                    cleared_count += 1

                    if verbose:
                        self.stdout.write(f'Cleared messages from session: {session.session_key[:8]}...')

            if cleared_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Cleared messages from {cleared_count} out of {total_sessions} sessions'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('No sessions with messages found')
                )

        self.stdout.write(
            self.style.SUCCESS('Message clearing completed!')
        )
