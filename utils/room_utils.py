from housing.models import Rooms, RoomTypes

def generate_rooms(hostel, room_type, num_rooms=1, **kwargs):
    for _ in range(num_rooms):
        Rooms.objects.create(
            room_type = room_type,
            comment = "",
            hostel = hostel
        )