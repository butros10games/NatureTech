from django.core.management.base import BaseCommand
from authentication.signals import page_refresh

class Command(BaseCommand):
    help = 'Sends a refresh command to the browser.'

    def handle(self, *args, **options):
        page_refresh.send(sender=None)

        self.stdout.write(self.style.SUCCESS('Successfully sent refresh command to the browser.'))
