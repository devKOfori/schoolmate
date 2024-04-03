from django.urls import path
from . import views
from housing import views as housing_views

urlpatterns = [
    path("all/", views.list_employee, name="list-employee"),
    path("my-employee/", views.my_employee, name="my-employee"),
    path("my-employees/update-role/", housing_views.HostelEmployeeAllocCreateView.as_view(), name="update-role")
]
