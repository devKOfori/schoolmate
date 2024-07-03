import os
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from hms.models import City

class Command(BaseCommand):
    help = "Import cities from a text file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="file path of cities data")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        try:
            with open(file_path, "r") as file:
                for name in file.readlines():
                    city, created = City.objects.get_or_create(name=name.strip())
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Sucess: {city} created successfully"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Error: {city} already exist"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: file not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))