from django.urls import path
from . import views as housing_views

urlpatterns = [
    #     path("create-hostel/",
    #          housing_views.CreateHostelView.as_view(),
    #          name="create-hostel"),
    path("my-hostel/", housing_views.my_hostel, name="my-hostel"),
    path(
        "my-hostel-blocks/", housing_views.get_my_hostel_blocks, name="my-hostel-blocks"
    ),
    path(
        "my-hostel-floors/", housing_views.get_my_hostel_floors, name="my-hostel-floors"
    ),
    path("my-hostel-rooms/", housing_views.get_my_hostel_rooms, name="my-hostel-rooms"),
    path("my-hostel-applications/", housing_views.get_my_hostel_applications, name="my-applications"),
    path(
        "my-hostel-roomtypes/",
        housing_views.get_my_hostel_roomtypes,
        name="my-hostel-roomtypes",
    ),
    path("create-hostel/", housing_views.create_hostel, name="create-hostel"),
    path("<slug:slugname>/", housing_views.configure_hostel, name="configure-hostel"),
    path(
        "<slug:slugname>/create-block/", housing_views.create_block, name="create-block"
    ),
    path(
        "<slug:slugname>/create-floor/", housing_views.create_floor, name="create-floor"
    ),
    path("<slug:slugname>/create-room/", housing_views.create_room, name="create-room"),
    path(
        "<slug:slugname>/create-roomtype/",
        housing_views.create_roomtype,
        name="create-roomtype",
    ),
]
