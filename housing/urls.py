from django.urls import path
from .import views

urlpatterns = [
#======================================================================================================================
#               VENDOR URLS
#======================================================================================================================
    path("vendors/all/", views.all_vendors, name="all-vendors"),
    path("vendors/my-vendor/", views.my_vendors, name="my-vendors"),
    path("vendors/create-vendor/", views.setup_vendor, name="create-vendor"),
    path("vendor/<str:vendor_id>/", views.vendor_detail, name="vendor-detail"),
#======================================================================================================================
#               HOSTEL URLS
#======================================================================================================================
    path("hostels/all", views.hostel_list, name="hostel-list"),
    path("hostels/my-hostels/", views.my_hostels, name="my-hostels"),
    path("register-tenant", views.register_tenant, name="register-tenant"),
    path("hostels/create-hostel/", views.create_hostel, name="create-hostel"),
    path("hostels/<str:hostel_id>/", views.hostel_detail, name="hostel-detail"),
    path("hostels/<str:hostel_id>/create-block/", views.create_block, name="create-block"),
    path("hostels/<str:hostel_id>/create-room/", views.create_room, name="create-room"),
    path("hostels/<str:hostel_id>/list-room/", views.room_list, name="list-room"),
#======================================================================================================================
#               OTHER URLS
#======================================================================================================================
    path("add-roomtype/", views.RoomTypeCreateView.as_view(), name="create-roomtype"),
    path("rooms/my-rooms/", views.MyHostelRoomListView.as_view(), name="my-rooms"),
    path("rooms/all/", views.all_rooms, name="all-rooms"),
    path("rooms/create-room/", views.RoomCreateView.as_view(), name="create-room"),
    path("rooms/requests/create-request/", views.request_room, name="create-request"),
    path("rooms/requests/all/", views.all_room_requests, name="all-room-requests"),
    path("rooms/requests/my-hostel-requests/", views.my_hostel_requests, name="my-hostel-requests"),
    # path("rooms/requests/<str:request_id>/", views.room_request_detail, name="room-request-detail"),
    path("rooms/<str:room_number>/", views.room_detail, name="room-detail"),
    path("assign-room/", views.assign_room, name="assign-room"),
    path("verify-property/all/", views.DocumentVerificationListView.as_view(), name="list-property-verification"),
    path("verify-property/<str:property_id>/", views.verify_property, name="verify-property"),
    path("verify-property/<str:property_id>/update", views.UpdateDocumentVerificationCreateView.as_view(), name="update-verification"),
]
