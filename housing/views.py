from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import models as housing_models
from . import forms as housing_forms

class CreateHostelView(generic.CreateView):
    model = housing_models.Hostels
    template_name = "housing/create_hostel.html"
    form_class = housing_forms.CreateHostelForm
    
    def get_success_url(self):
        return reverse_lazy("configure-hostel", kwargs={"nameslug": self.object.nameslug})


def configure_hostel(request, nameslug):
    hostel = housing_models.Hostels.objects.get(nameslug=nameslug)
    context = {
        "hostel": hostel
    }
    return render(request, "housing/configure_hostel.html",
                   context)

