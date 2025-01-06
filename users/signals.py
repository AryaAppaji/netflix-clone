from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import CustomUser
from finance.models import Subscription, UserSubscription
from django.utils.timezone import now, timedelta


@receiver(post_save, sender=CustomUser)
def handle_user_registration(sender, instance, created, **kwargs):
    if created:
        # Assigning Subscription.
        subscription_details = Subscription.objects.filter(
            name__exact="Trail"
        ).first()

        subscription_end_date = now() + timedelta(
            days=subscription_details.validity
        )

        UserSubscription.objects.create(
            user=instance,
            subscription=subscription_details,
            end_date=subscription_end_date,
            is_current_subscription=True,
        )

        # Sending email.
        # Only send the email when a new user is created (not updated)
        subject = "Welcome to Our Service!"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.email  # recipient's email address

        # Render the HTML template
        html_message = render_to_string("users/registration_successful.html", {
            "days": subscription_details.validity,
        })

        # Send the email
        send_mail(
            subject=subject,
            message="",  # We don't need plain text body because we are using HTML
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message,
        )        
