from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class CommandBasic(BaseCommand):
    just_for_debug_mode = False

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='[.args]', nargs='*', help='args',
        )

    def handle(self, *args, **options):
        if self.just_for_debug_mode and not settings.DEBUG:
            self.stdout.write("Only work on debug mode!")
            return
        self.run(self, *args, **options)

    def run(self, *args, **options):
        raise NotImplementedError
