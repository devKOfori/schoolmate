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
                for line in file.readlines():
                    room_category, room_type = line.strip().split(" ", maxsplit=1)
                    room_type = room_type.strip("\n")
                    room_category = housing_models.RoomCategories.objects.get(
                        name=room_category
                    )
                    # print(room_category)
                    room_type, created = housing_models.RoomTypes.objects.get_or_create(
                        room_type=room_type, category=room_category
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Success: {room_type} created successfully"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Error: failed to create {room_category}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Error: file not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: an error occured {e}"))
