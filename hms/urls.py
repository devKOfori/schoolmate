from django.urls import path
from . import views
import housing.views as housing_views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("dashboard/", views.staff_dashboard, name="dashboard"),
    path("dashboard-index/", views.staff_dashboard_index, name="dashboard_index"),
    path("search-hostel/", housing_views.search_hostel, name="search-hostel"),
    path(
        "search-application/",
        housing_views.search_application,
        name="search-application",
    ),
    path(
        "submit-application/",
        housing_views.submit_application,
        name="submit-application",
    ),
    path("application-sent/", housing_views.application_sent, name="application-sent"),
    path(
        "find-application/",
        housing_views.find_application,
        name="find-application",
    ),
    path(
        "my-offers/<str:application_code>/",
        housing_views.housing_offer_details,
        name="my-offer-details",
    ),
]
