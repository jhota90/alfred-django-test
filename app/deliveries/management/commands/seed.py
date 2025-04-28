import random

from deliveries.models import Address, Driver
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = "Seed database with addresses and drivers"

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write("Seeding data...")

        # Create 20 address
        addresses = []
        for _ in range(20):
            address = Address.objects.create(
                street=fake.address(),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
            )
            addresses.append(address)

        self.stdout.write(self.style.SUCCESS("Created 20 addresses"))

        # Crete 20 drivers
        for _ in range(20):
            Driver.objects.create(
                name=fake.name(), current_address=random.choice(addresses)
            )

        self.stdout.write(self.style.SUCCESS("Created 20 drivers"))
