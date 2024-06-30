from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("dashboard/", views.staff_dashboard, name="dashboard"),
]
