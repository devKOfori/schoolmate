from typing import Any
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from housing import models as housing_models

class Command(BaseCommand):
    help = "import room categories data from .txt file"

    def add_arguments(self, parser):
        return parser.add_argument("file_path", type=str, help="room categories file path")
    
    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        try:
            with open(file_path, "r") as file:
                for room_category in file.readlines():
                    room_category, created = housing_models.RoomCategories.objects.get_or_create(
                        name=room_category.strip("\n"), description=""
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Success: {room_category} created successfully"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Error: failed to create {room_category}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Error: file not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: an error occured {e}"))
