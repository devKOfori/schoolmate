from django.shortcuts import render

# Create your views here.

def index(request):
    return render(
        request, 
        "hms/index.html"
    )

def staff_dashboard(request):
    return render(request, "hms/hostel_staff_dashboard.html")