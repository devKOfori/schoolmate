from django.urls import path
from . import views

urlpatterns = [
    path("all/", views.list_employee, name="list-employee"),
    path("my-employee/", views.my_employee, name="my-employee"),
]
