from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
import housing.models as housing_models

# Create your views here.


def index(request):
    top_10_rated = housing_models.Hostels.objects.order_by("-rating")[:10]
    context = {"hostels": top_10_rated}
    return render(request, "hms/index.html", context)


def staff_dashboard(request):
    return render(request, "hms/hostel_staff_dashboard.html")


def staff_dashboard_index(request):
    try:
        request.user.hostel
        return render(request, "hms/dashboard_index.html")
    except ObjectDoesNotExist:
        return render(request, "housing/hostels/no-hostel.html")
