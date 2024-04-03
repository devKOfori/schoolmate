from django.urls import path
from . import views
from housing.views import update_employee_role

urlpatterns = [
    path("all/", views.list_employee, name="list-employee"),
    path("my-employee/", views.my_employee, name="my-employee"),
    path("my-employees/update-role/", update_employee_role, name="update-role")
]
