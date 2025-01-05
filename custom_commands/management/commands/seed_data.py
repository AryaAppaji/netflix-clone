from django.core.management.base import BaseCommand
from finance.seeders import (
    seed_subscriptions,
)


class Command(BaseCommand):
    help = "Seeds intial data"

    def handle(self, *args, **options):
        seed_subscriptions()
        self.stdout.write(self.style.SUCCESS("Seeders ran successfully"))
