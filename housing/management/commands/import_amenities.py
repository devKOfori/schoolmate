from django.core.management import BaseCommand
from housing import models as housing_model

class Command(BaseCommand):
    help = "import amenities data from .txt file"

    def add_arguments(self, parser):
        parser.add_argument("file_path")
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        file_path = options["file_path"]
        try:
            with open(file_path, "r") as file:
                for line in file.readlines():
                    amenity_name = line.strip("\n")
                    amenity, created = housing_model.Amenities.objects.get_or_create(
                        name = amenity_name
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Success: {amenity} created successfully"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Error: {amenity} already exist"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Error: file not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: an error occured {e}"))
