from django.db.models.base import Model as Model
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from . import models as housing_models
from . import forms as housing_forms
from hms import models as hms_models
from accounts import models as accounts_models
import uuid
from django.contrib import messages

class CreateHostelView(generic.CreateView):
    model = housing_models.Hostels
    template_name = "housing/create_hostel.html"
    form_class = housing_forms.CreateHostelForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities = hms_models.City.objects.all()
        context["cities"] = cities
        return context
    
    def form_valid(self, form):
        # self.object = self.get_object()
        form.instance.id = uuid.uuid4()
        form.instance.name = self.request.POST.get("name")
        form.instance.regNumber = self.request.POST.get("regNumber")
        form.instance.address = self.request.POST.get("address")
        city_id = self.request.POST.get("city")
        city = hms_models.City.objects.get(id=city_id)
        form.instance.city = city
        form.instance.postalcode = self.request.POST.get("postalcode")
        form.instance.latitude = self.request.POST.get("latitude")
        form.instance.longitude = self.request.POST.get("longitude")
        form.instance.phone = self.request.POST.get("phone")
        form.instance.email = self.request.POST.get("email")
        user = self.request.user
        createdby = accounts_models.CustomUser.objects.get(email=user.email)
        form.instance.createdby = createdby

        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("errors in form")
        print(form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
        id_str = str(self.get_form().instance.id)
        url = reverse("configure-hostel", kwargs={"id":id_str})
        return redirect(url)


def create_hostel(request):
    cities = hms_models.City.objects.all()
    context = {"cities": cities}
    if request.method == "POST":
        id = uuid.uuid4()
        name = request.POST.get("name")
        regNumber = request.POST.get("regNumber", None)
        address = request.POST.get("address")
        city_id = request.POST.get("city", None)
        city = hms_models.City.objects.get(id=city_id)
        postalcode = request.POST.get("postalcode", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        phone = request.POST.get("phone", None)
        email = request.POST.get("email", None)
        user = request.user
        createdby = accounts_models.CustomUser.objects.get(email=user.email)
        hostel = housing_models.Hostels.objects.create(
            name=name, regNumber=regNumber,
            address=address, city=city,
            postalcode=postalcode, latitude=latitude,
            longitude=longitude, phone=phone,
            email=email, createdby=createdby
        )
        return redirect(reverse("configure-hostel", kwargs={"slugname":hostel.nameslug}))
    else:
        return render(request, "housing/create_hostel.html", context)
    
def configure_hostel(request, slugname):
    hostel = housing_models.Hostels.objects.get(nameslug=slugname)
    context = {
        "hostel": hostel
    }
    return render(request, "housing/configure_hostel.html",
                   context)

