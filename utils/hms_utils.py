from accounts import models as account_models

def generate_regions():
    regions_file_path = "../data/regions.txt"
    with open(regions_file_path, "r") as file:
        for region_name in file:
            region = account_models.Region.objects.create(name=region_name)
            