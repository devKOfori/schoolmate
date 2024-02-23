from django.shortcuts import render, redirect
from .forms import (
    TenantCreationForm, HostelCreationForm, HostelAddressForm,
    BlockCreationForm, RoomCreationForm, RoomAssignmentForm
)
from accounts.forms import (
    UserCreationForm
)
from .models import (
    HostelStatus, Hostel, Room
)
from django.urls import reverse
from django.shortcuts import get_object_or_404
# Create your views here.


def register_tenant(request):
    user_form = UserCreationForm(prefix="user")
    tenant_form = TenantCreationForm(prefix="tenant")
    if request.method == "POST":
        user_form = UserCreationForm(request.POST, prefix="user")
        tenant_form = TenantCreationForm(request.POST, prefix="tenant")
        if user_form.is_valid() and tenant_form.is_valid():
            user = user_form.save()
            tenant = tenant_form.save(commit=False)
            tenant.user = user
            tenant.email = user.email
            tenant.save()
            return redirect(reverse("login"))
        return render(request, "housing/tenant_creation.html", {"user_form": user_form, "tenant_form": tenant_form, "error_message": "Error somewhere"})
    else:
        return render(request, "housing/tenant_creation.html", {"user_form": user_form, "tenant_form": tenant_form})
    
def create_hostel(request):
    hostel_form = HostelCreationForm(prefix="hostel")
    hostel_address_form = HostelAddressForm(prefix="address")
    default_hostel_status = HostelStatus.objects.first()
    if request.method == "POST":
        hostel_form = HostelCreationForm(request.POST, prefix="hostel")
        hostel_address_form = HostelAddressForm(request.POST, prefix="address")
        if hostel_form.is_valid() and hostel_address_form.is_valid():
            hostel = hostel_form.save(commit=False)
            hostel.created_by = request.user
            # hostel.warden = request.user
            hostel.status = default_hostel_status
            hostel.save()
            address = hostel_address_form.save(commit=False)
            address.hostel = hostel
            address.save()
            return redirect(reverse("hostel-detail", kwargs={"hostel_id": hostel.hostel_id}))
        return render(request, "housing/create_hostel.html", {"hostel_form": hostel_form, "address_form": hostel_address_form})
    else:
        return render(request, "housing/create_hostel.html", {"hostel_form": hostel_form, "address_form": hostel_address_form})
    
def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, hostel_id=hostel_id)
    hostel_rooms = Room.objects.filter(hostel=hostel)
    context = {
        "hostel": hostel,
        "rooms": hostel_rooms
    }
    return render(request, "housing/hostel_detail.html", context)

def hostel_list(request):
    hostels = Hostel.objects.all()
    context = {
        "hostels": hostels
    }
    return render(request, "housing/hostel_list.html", context=context)

def create_block(request, hostel_id):
    hostel = get_object_or_404(Hostel, hostel_id = hostel_id)
    block_form = BlockCreationForm()
    context = {"hostel": hostel, "block_form": block_form}
    if request.method == "POST":
        block_form = BlockCreationForm(request.POST)
        if block_form.is_valid():
            block = block_form.save(commit=False)
            block.hostel = hostel
            block.save()
            return redirect(reverse("hostel-detail", kwargs={"hostel_id":hostel.hostel_id}))
        context["block_form"] = block_form
        return render(request, "housing/create_block.html", context)
    else:
        return render(request, "housing/create_block.html", context)
    
def create_room(request, hostel_id):
    hostel = get_object_or_404(Hostel, hostel_id = hostel_id)
    room_form = RoomCreationForm()
    context = {"hostel": hostel, "room_form": room_form}
    if request.method == "POST":
        room_form = RoomCreationForm(request.POST)
        if room_form.is_valid():
            room = room_form.save(commit=False)
            room.hostel = hostel
            room.save()
            return redirect(reverse("room-detail", kwargs={
                "room_number": room.room_number
            }))
        context["room_form"] = room_form
    else:
        return render(request, "housing/create_room.html", context)
    
def room_detail(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    # room = Room.objects.get(room_number = room_number)
    context = {
        "room": room
    }
    return render(request, "housing/room_detail.html", context)

def room_list(request, hostel_id):
    hostel = get_object_or_404(Hostel, hostel_id=hostel_id)
    rooms = Room.objects.filter(hostel=hostel)
    context = {
        "rooms": rooms
    }
    return render(request, "housing/room_list.html", context)

def all_rooms(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms
    }
    return render(request, "housing/room_list.html", context)

def assign_room(request):
    room_assignment_form = RoomAssignmentForm()
    context = {"room_assignment_form":room_assignment_form}
    if request.method == "POST":
        room_assignment_form = RoomAssignmentForm(request.POST)
        if room_assignment_form.is_valid():
            room_assignment = room_assignment_form.save()
            return redirect(reverse("room-detail", kwargs={"room_number": room_assignment.room.room_number}))
        context["room_assignment_form"] = room_assignment_form
        return render(request, "housing/assign_room.html", context)
    else:
        return render(request, "housing/assign_room.html", context)