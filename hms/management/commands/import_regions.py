from typing import Any
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from hms.models import Region

class Command(BaseCommand):
    help = "Import Regions data from text file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="file path for regions data")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        try:
            with open(file_path, "r") as file:
                for line in file.readlines():
                    region, created = Region.objects.get_or_create(name = line.strip())
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Region {line} created successfully"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Error: {line} already exist"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: File not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))