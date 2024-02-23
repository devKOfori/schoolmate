from django.urls import path
from .import views

urlpatterns = [
    path("hostels", views.hostel_list, name="hostel-list"),
    path("assign-room/", views.assign_room, name="assign-room"),
    path("register-tenant", views.register_tenant, name="register-tenant"),
    path("create-hostel/", views.create_hostel, name="create-hostel"),
    path("<str:hostel_id>/", views.hostel_detail, name="hostel-detail"),
    path("<str:hostel_id>/add-block", views.create_block, name="create-block"),
    path("<str:hostel_id>/add-room", views.create_room, name="create-room"),
    path("<str:hostel_id>/list-room", views.room_list, name="list-room"),
    path("rooms/all/", views.all_rooms, name="all-rooms"),
    path("rooms/<str:room_number>/", views.room_detail, name="room-detail"),
    path("create-vendor", views.setup_vendor, name="create-vendor"),
    path("vendor/<str:vendor_id>/", views.vendor_detail, name="vendor-detail"),
]
