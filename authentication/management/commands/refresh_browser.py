import os

from django.core.management.base import BaseCommand

from authentication.signals import page_refresh


class Command(BaseCommand):
    help = "Sends a refresh command to the browser and touches the .manage file."

    def handle(self, *args, **options):

        # Touch the .manage file
        with open(".manage", "a"):
            os.utime(".manage", None)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully sent refresh command to the browser and touched the .manage file."
            )
        )
