#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

test_email = 'saairamgowshik@gmail.com'
print(f'Testing lookup for: {test_email}')
print(f'With strip/lower: {test_email.strip().lower()}')

# Test 1: Exact email match
try:
    u = User.objects.get(email=test_email)
    print(f'✓ Exact match - Found user: {u.username}, Email: {u.email}')
except User.DoesNotExist:
    print(f'✗ Exact match - User not found')

# Test 2: Case-insensitive email match
try:
    u = User.objects.get(email__iexact=test_email.strip().lower())
    print(f'✓ Case-insensitive - Found user: {u.username}, Email: {u.email}')
except User.DoesNotExist:
    print(f'✗ Case-insensitive - User not found')

# List all users
print('\nAll users in database:')
for user in User.objects.all():
    print(f'  - Username: {user.username}, Email: {user.email}')
