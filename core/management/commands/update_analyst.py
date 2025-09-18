from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Update financial analyst username and email.'

    def handle(self, *args, **options):
        try:
            u = User.objects.get(username='hr@abcinc.com')
            u.username = 'divagar0308@gmail.com'
            u.email = 'divagar0308@gmail.com'
            u.save()
            self.stdout.write(self.style.SUCCESS('Updated analyst username and email to divagar0308@gmail.com'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User hr@abcinc.com not found.'))