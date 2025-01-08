from django.core.management.base import BaseCommand
from finance.seeders import (
    seed_subscriptions,
)
from users.seeders import (
    seed_users,
)


class Command(BaseCommand):
    help = "Seeds intial data"

    def handle(self, *args, **options):
        seed_subscriptions()
        seed_users()
        self.stdout.write(self.style.SUCCESS("Seeders ran successfully"))
