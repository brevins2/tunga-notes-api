from django.core.mail import send_mail

def send_password_reset_email(to_email, reset_link):
    subject = 'Password Reset for Tunganotes'
    message = f'Click the following link to reset your password: {reset_link}'
    from_email = 'admin@tunganotes.com'  # Replace with your app's email address
    recipient_list = [to_email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_note_sharing_email(to_email, note_link, note_title):
    subject = f'Shared Note: {note_title}'
    message = f'Here is the link to the shared note: {note_link}'
    from_email = 'admin@tunganotes.com'  # Replace with your app's email address
    recipient_list = [to_email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
