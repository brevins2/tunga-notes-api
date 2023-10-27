from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_email(to_email, reset_link):
    subject = 'Password Reset for Tunganotes'
    message = f'Click the following link to reset your password: {reset_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

