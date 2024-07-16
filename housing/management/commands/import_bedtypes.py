from django.core.management import BaseCommand
from housing import models as housing_model

class Command(BaseCommand):
    help = "import amenities data from .txt file"

    def add_arguments(self, parser):
        parser.add_argument("file_path")
    
    def handle(self, *args, **kwargs) -> str | None:
        file_path = kwargs["file_path"]
        try:
            with open(file_path, "r") as file:
                for line in file.readlines():
                    bed_type = line.strip("\n")
                    bed_type, created = housing_model.BedTypes.objects.get_or_create(
                        bed_type = bed_type
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Success: {bed_type} created successfully"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Error: {bed_type} already exist"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Error: file not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: an error occured {e}"))
