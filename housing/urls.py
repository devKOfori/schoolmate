from django.urls import path
from .import views as housing_views

urlpatterns = [
#     path("create-hostel/", 
#          housing_views.CreateHostelView.as_view(), 
#          name="create-hostel"),
    path("create-hostel/", 
         housing_views.create_hostel, 
         name="create-hostel"),
    path("<slug:slugname>/",
         housing_views.configure_hostel, 
         name="configure-hostel")

]
