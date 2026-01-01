from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    help = 'Ensures superuser exists using environment variables'

    def handle(self, *args, **kwargs):
        username = config('SUPERUSER_USERNAME', default='admin')
        email = config('SUPERUSER_EMAIL', default='admin@orbis.com')
        password = config('SUPERUSER_PASSWORD', default='changeme')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists')
            )
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {email}')
            )
