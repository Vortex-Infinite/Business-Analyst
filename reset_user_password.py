#!/usr/bin/env python
"""
Password Reset Utility for ORBIS
Allows admin to reset a user's password and send it via email
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.otp_utils import send_credentials_email
import string
import random

User = get_user_model()

def generate_password(username, length=25):
    """Generate password as username@(random 25 chars)"""
    chars = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(length))
    return f"{username}@{random_part}"

def reset_password(email):
    """Reset password for a user by email"""
    try:
        user = User.objects.get(email__iexact=email.strip().lower())
        print(f"Found user: {user.username} ({user.email})")
        
        # Generate new password
        new_password = generate_password(user.username)
        user.set_password(new_password)
        user.save()
        
        print(f"Password reset successfully!")
        print(f"New password: {new_password}")
        
        # Send email
        send_credentials_email(user, new_password)
        print(f"Credentials email sent to: {user.email}")
        
        return True
    except User.DoesNotExist:
        print(f"ERROR: User with email '{email}' not found")
        print("\nAvailable users:")
        for u in User.objects.all():
            print(f"  - {u.email} (username: {u.username})")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ORBIS Password Reset Utility")
    print("=" * 60)
    
    email = input("\nEnter user email: ").strip()
    
    if email:
        reset_password(email)
    else:
        print("No email provided")
