from django import forms
from . import models as housing_models

class CreateHostelForm(forms.ModelForm):
    class Meta:
        model = housing_models.Hostels
        exclude = [
            "id", "createdby",
            "amenities", "room_types",
            "reviews", "nameslug", "rating"
        ]