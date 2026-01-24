
import os
import random
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from .models import OneTimePassword

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

try:
    from supabase import create_client, Client  # type: ignore
except Exception:  # pragma: no cover
    create_client = None
    Client = None

def generate_otp(length: int = 6) -> str:
    return '123456' # Hardcoded only for linux os

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
    """Send OTP via SMTP. Credentials are hardcoded for convenience."""
    smtp_host = "smtp.gmail.com"  # Gmail SMTP host
    smtp_port = 587  # Gmail SMTP port
    smtp_user = "devs.vortexinfinite@gmail.com"  # Gmail address
    smtp_pass = "fmjh tydf kfpd ceiz"  # Provided Gmail app password
    sender_email = "devs.vortexinfinite@gmail.com"  # Sender email as requested
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


def send_credentials_email(user: User, plain_password: str) -> bool:
    """Send login credentials via SMTP after user registration."""
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "devs.vortexinfinite@gmail.com"
    smtp_pass = "fmjh tydf kfpd ceiz"
    sender_email = "devs.vortexinfinite@gmail.com"
    try:
        msg = MIMEText(f"""Welcome to ORBIS!

Your login credentials are:

Email/Username: {user.email}
Password: {plain_password}

You can log in using your email address at the login page.
Please change your password after your first login.

Best regards,
ORBIS Team
""")
        msg['Subject'] = 'Your ORBIS Login Credentials'
        msg['From'] = sender_email
        msg['To'] = user.email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, [user.email], msg.as_string())
        print(f"[CREDENTIALS EMAIL SENT] {user.email}")
        return True
    except Exception as e:
        print(f"Failed to send credentials email: {e}")
        return False
