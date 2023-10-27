from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from ..Notes import settings
from .models import Notes

@shared_task
def send_due_date_reminders():
    # Get notes with due dates that are approaching or have expired
    current_time = timezone.now()
    notes = Notes.objects.filter(due_date=current_time)

    for note in notes:
        # Check if the due date is in the past or within a certain time frame
        # You can customize this logic based on your requirements
        if (note.due_date - current_time).days <= 7:
            # Send a reminder email
            subject = f"Reminder: Note Due Date Approaching"
            message = f"Your note '{note.title}' is due on {note.due_date}. Don't forget to complete it!"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [note.user]  # Assuming 'user' is the owner of the note

            send_mail(subject, message, from_email, recipient_list)
