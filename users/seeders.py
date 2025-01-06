from .models import CustomUser

def seed_users():
    if not CustomUser.objects.filter(username="nfcadmin"):
        CustomUser.objects.create_superuser(
            username="nfcadmin",
            email='admin@nfc.com',
            password='admin@123',
            mobile_number="9876543210",
        )