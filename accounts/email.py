from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User


def send_otp(email):
    subject = 'Your Account verification mail'
    otp = random.randint(100000, 999999)
    msg = f'Your OTP to activate your account {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, msg, email_from, [email])
    user = User.objects.get(email=email)
    user.otp = otp
    user.save()
