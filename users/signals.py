from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # Only send the email when a new user is created (not updated)
        subject = "Welcome to Our Service!"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.email  # recipient's email address

        # Render the HTML template
        html_message = render_to_string("users/registration_successful.html")

        # Send the email
        send_mail(
            subject,
            "",  # We don't need plain text body because we are using HTML
            from_email,
            [to_email],
            html_message=html_message,
        )
