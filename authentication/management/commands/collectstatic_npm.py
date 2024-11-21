import subprocess

from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectstaticCommand,
)


class Command(CollectstaticCommand):
    def handle(self, *args, **options):
        # First, run the standard collectstatic command
        super().handle(*args, **options)

        # Then run 'npm run build:css'
        self.stdout.write("Running 'npm run build:css'...")
        subprocess.call(["npm", "run", "watch:css"])
