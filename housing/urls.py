from django.urls import path
from .import views as housing_views

urlpatterns = [
#     path("create-hostel/", 
#          housing_views.CreateHostelView.as_view(), 
#          name="create-hostel"),
    path("create-hostel/", housing_views.create_hostel, name="create-hostel"),
    path("<slug:slugname>/", housing_views.configure_hostel, name="configure-hostel"),
    path("<slug:slugname>/create-block/", housing_views.create_block, name="create-block") ,
    path("<slug:slugname>/create-floor/", housing_views.create_floor, name="create-floor") ,

]
