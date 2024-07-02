from django import forms
from . import models as housing_models

class CreateHostelForm(forms.ModelForm):
    class Meta:
        model = housing_models.Hostels
        exclude = [
            "amenities", "room_types",
            "reviews"
        ]