from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create test users for the application'

    def handle(self, *args, **options):
        # Create HR user
        hr_user, created = User.objects.get_or_create(
            username='hr@abcinc.com',
            defaults={
                'email': 'hr@abcinc.com',
                'password': make_password('password'),
                'first_name': 'HR',
                'last_name': 'Manager',
                'is_staff': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created HR user: hr@abcinc.com / password')
            )
        else:
            self.stdout.write(
                self.style.WARNING('HR user already exists: hr@abcinc.com')
            )

        # Create Employee user
        employee_user, created = User.objects.get_or_create(
            username='employee@abcinc.com',
            defaults={
                'email': 'employee@abcinc.com',
                'password': make_password('password'),
                'first_name': 'John',
                'last_name': 'Employee',
                'is_staff': False,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Employee user: employee@abcinc.com / password')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Employee user already exists: employee@abcinc.com')
            )

        # Create a superuser for admin access
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@abcinc.com',
                'password': make_password('admin123'),
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Admin user: admin / admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists: admin')
            )

        self.stdout.write(
            self.style.SUCCESS('Test users setup completed!')
        )

