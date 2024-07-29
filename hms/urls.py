from django.urls import path
from . import views
import housing.views as housing_views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("dashboard/", views.staff_dashboard, name="dashboard"),
    path("dashboard-index/", views.staff_dashboard_index, name="dashboard_index"),
    path("search-hostel/", housing_views.search_hostel, name="search-hostel"),
    path("submit-application/", housing_views.submit_application, name="submit-application"),
]
