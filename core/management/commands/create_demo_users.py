from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create demo users for authentication testing'

    def handle(self, *args, **options):
        # Create manager user
        if not User.objects.filter(username='manager@orbis.com').exists():
            manager = User.objects.create_user(
                username='manager@orbis.com',
                email='manager@orbis.com',
                password='password'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created manager user: {manager.username}')
            )
        else:
            self.stdout.write(f'Manager user already exists')

        # Create analyst user
        if not User.objects.filter(username='analyst@abcinc.com').exists():
            analyst = User.objects.create_user(
                username='analyst@abcinc.com',
                email='analyst@abcinc.com',
                password='password'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created analyst user: {analyst.username}')
            )
        else:
            self.stdout.write(f'Analyst user already exists')

        # List all users
        self.stdout.write('\nAll users:')
        for user in User.objects.all():
            self.stdout.write(f'  - {user.username} ({user.email})')
