
import os
import random
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from .models import OneTimePassword
from decouple import config


try:
    from supabase import create_client, Client  # type: ignore
except Exception:  # pragma: no cover
    create_client = None
    Client = None

def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices('0123456789', k=length))

def create_otp_for_user(user: User, ttl_minutes: int = 5) -> OneTimePassword:
    # Invalidate previous unused OTPs for login
    OneTimePassword.objects.filter(user=user, purpose='login', is_used=False).update(is_used=True)
    code = generate_otp()
    otp = OneTimePassword.objects.create(
        user=user,
        code=code,
        purpose='login',
        expires_at=timezone.now() + timedelta(minutes=ttl_minutes)
    )
    return otp

def send_otp_email(user: User, otp: OneTimePassword) -> bool:
    """Send OTP via SMTP using environment variables for credentials."""
    smtp_host = config('EMAIL_HOST', default='smtp.gmail.com')
    smtp_port = config('EMAIL_PORT', default=587, cast=int)
    smtp_user = config('EMAIL_HOST_USER')
    smtp_pass = config('EMAIL_HOST_PASSWORD')
    sender_email = config('EMAIL_FROM', default=smtp_user)
    try:
        msg = MIMEText(f"Your ORBIS login OTP is: {otp.code}\nThis code expires in 5 minutes.")
        msg['Subject'] = 'Your ORBIS Login OTP'
        msg['From'] = sender_email
        msg['To'] = user.email  # Always sends to the analyst's entered email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, [user.email], msg.as_string())
        print(f"[EMAIL SENT] {user.email} -> {otp.code}")
        return True
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        return False

def verify_otp(user: User, code: str) -> bool:
    try:
        otp = OneTimePassword.objects.filter(user=user, purpose='login', code=code, is_used=False).latest('created_at')
    except OneTimePassword.DoesNotExist:
        return False
    if otp.is_expired():
        return False
    otp.is_used = True
    otp.save(update_fields=['is_used'])
    return True
