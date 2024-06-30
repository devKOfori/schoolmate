import uuid
import os
from django.utils.text import slugify

def generate_hostel_image_upload_path(instance, filename):
    hostel_name = instance.hostel.name
    hostel_folder = slugify(hostel_name)
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid.uuid4}{ext}"
    path = os.path.join("photos", "hostels", hostel_folder, new_filename)
    return path