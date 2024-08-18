from django.db.models.base import Model as Model
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from . import models as housing_models
from . import forms as housing_forms
from hms import models as hms_models
from accounts import models as accounts_models
import uuid
from django.contrib import messages
from utils.room_utils import generate_rooms
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


default_application_status = housing_models.ApplicationStatus.objects.get(
    name="Pending"
)


class CreateHostelView(generic.CreateView):
    model = housing_models.Hostels
    template_name = "housing/create_hostel.html"
    form_class = housing_forms.CreateHostelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities = hms_models.City.objects.all()
        context["cities"] = cities
        return context

    def form_valid(self, form):
        # self.object = self.get_object()
        form.instance.id = uuid.uuid4()
        form.instance.name = self.request.POST.get("name")
        form.instance.regNumber = self.request.POST.get("regNumber")
        form.instance.address = self.request.POST.get("address")
        city_id = self.request.POST.get("city")
        city = hms_models.City.objects.get(id=city_id)
        form.instance.city = city
        form.instance.postalcode = self.request.POST.get("postalcode")
        form.instance.latitude = self.request.POST.get("latitude")
        form.instance.longitude = self.request.POST.get("longitude")
        form.instance.phone = self.request.POST.get("phone")
        form.instance.email = self.request.POST.get("email")
        user = self.request.user
        createdby = accounts_models.CustomUser.objects.get(email=user.email)
        form.instance.createdby = createdby

        return super().form_valid(form)

    def form_invalid(self, form):
        print("errors in form")
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        id_str = str(self.get_form().instance.id)
        url = reverse("configure-hostel", kwargs={"id": id_str})
        return redirect(url)


def my_hostel(request):
    user = request.user
    # my_hostel = housing_models.Hostels.objects.get(createdby=user)
    # my_hostel = get_object_or_404(housing_models.Hostels, createdby=user)
    try:
        my_hostel = housing_models.Hostels.objects.get(createdby=user)
        print(my_hostel)
        context = {"my_hostel": my_hostel}
        return render(request, "housing/my-hostel.html", context)
    except ObjectDoesNotExist:
        return render(request, "housing/hostels/no-hostel.html", {"user": user})


def create_hostel(request):
    cities = hms_models.City.objects.all()
    context = {"cities": cities}
    hostel_form = housing_forms.CreateHostelForm()
    if request.method == "POST":
        # # id = uuid.uuid4()
        # form = housing_forms.CreateHostelForm(request.POST)
        # if form.is_valid():
        #     print("hey...")
        #     hostel = form.save()
        # else:
        #     print(form.errors)
        #     print("nay...")
        name = request.POST.get("name")
        regNumber = request.POST.get("regNumber", None)
        address = request.POST.get("address")
        city_id = request.POST.get("city", None)
        city = hms_models.City.objects.get(id=city_id)
        postalcode = request.POST.get("postalcode", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        phone = request.POST.get("phone", None)
        email = request.POST.get("email", None)
        user = request.user
        createdby = accounts_models.CustomUser.objects.get(email=user.email)
        hostel = housing_models.Hostels.objects.create(
            name=name,
            regNumber=regNumber,
            address=address,
            city=city,
            postalcode=postalcode,
            latitude=latitude,
            longitude=longitude,
            phone=phone,
            email=email,
            createdby=createdby,
        )
        # return render(request, "housing/create_hostel.html", context)
        return redirect(
            reverse("configure-hostel", kwargs={"slugname": hostel.nameslug})
        )
    else:
        return render(request, "housing/create_hostel.html", context)


def configure_hostel(request, slugname):
    hostel = housing_models.Hostels.objects.get(nameslug=slugname)
    my_amenities = hostel.amenities.all()
    all_amenities = housing_models.Amenities.objects.all()
    blocks = housing_models.Blocks.objects.filter(hostel=hostel)
    floors = housing_models.Floors.objects.filter(block__hostel=hostel)
    context = {
        "hostel": hostel,
        "my_amenities": my_amenities,
        "all_amenities": all_amenities,
        "blocks": blocks,
        "floors": floors,
    }
    return render(request, "housing/configure_hostel.html", context)


def get_my_hostel_blocks(request):
    user = request.user
    try:
        blocks = user.hostel.blocks.all()
        context = {"hostel": user.hostel, "blocks": blocks}
        return render(request, "housing/blocks/my-hostel-blocks.html", context)
    except ObjectDoesNotExist:
        return render(request, "housing/hostels/no-hostel.html", {"user": user})


def get_my_hostel_floors(request):
    user = request.user
    try:
        hostel = housing_models.Hostels.objects.prefetch_related("blocks__floors").get(
            id=user.hostel.id
        )
        for block in hostel.blocks.all():
            print(f"Block: {block.name}")
            for floor in block.floors.all():
                print(f"  Floor: {floor.name}")
        context = {"hostel_data": hostel}
        return render(request, "housing/blocks/my-hostel-floors.html", context)
    except:
        return render(request, "housing/hostels/no-hostel.html", {"user": user})


def get_my_hostel_rooms(request):
    user = request.user
    try:
        hostel = housing_models.Hostels.objects.prefetch_related("rooms").get(
            id=user.hostel.id
        )
        context = {"hostel": hostel}
        return render(request, "housing/rooms/my-hostel-rooms.html", context)
    except ObjectDoesNotExist:
        return render(request, "housing/hostels/no-hostel.html", {"user": user})


def get_my_hostel_roomtypes(request):
    user = request.user
    try:
        hostel = user.hostel
        my_room_types = housing_models.HostelRoomTypes.objects.filter(hostel=hostel)
        context = {"hostel": hostel, "my_room_types": my_room_types}
        return render(request, "housing/rooms/my-hostel-roomtypes.html", context)
    except:
        return render(request, "housing/hostels/no-hostel.html", {"user": user})


def get_my_hostel_applications(request):
    user = request.user
    user_hostel = user.hostel
    message = messages.get_messages(request)
    context = {"messages": message}
    try:
        applications = housing_models.ApplicationHostel.objects.filter(
            hostel=user_hostel
        )
        context = {"applications": applications}
        return render(request, "housing/hostels/my-applications.html", context)
    except Exception as e:
        print(f"An error occured: {e}")
        return redirect(reverse_lazy("dashboard"))


def create_block(request, slugname):
    print(slugname)
    hostel = get_object_or_404(housing_models.Hostels, nameslug=slugname)
    context = {"hostel": hostel}
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        createdby = request.user
        _ = housing_models.Blocks.objects.create(
            name=name, description=description, hostel=hostel, createdby=createdby
        )
        return redirect(reverse_lazy("dashboard"))
    else:
        return render(request, "housing/create-block.html", context)


def create_floor(request, slugname):
    hostel = get_object_or_404(housing_models.Hostels, nameslug=slugname)
    context = {"hostel": hostel}
    if request.method == "POST":
        name = request.POST.get("name")
        print(name)
        description = request.POST.get("description")
        print(description)
        block_id = request.POST.get("block")
        block = housing_models.Blocks.objects.get(id=block_id)
        createdby = request.user
        _ = housing_models.Floors.objects.create(
            name=name, description=description, block=block, createdby=createdby
        )
        return redirect(reverse_lazy("dashboard"))
    else:
        blocks = housing_models.Blocks.objects.filter(hostel__nameslug=slugname)
        context["blocks"] = blocks
        return render(request, "housing/create_floor.html", context)


def create_roomtype(request, slugname):
    hostel = get_object_or_404(housing_models.Hostels, nameslug=slugname)
    context = {}
    context["hostel"] = hostel
    request_data = {}
    if request.method == "POST":
        request_data["room_type"] = request.POST.get("roomtype")
        request_data["number_of_rooms"] = request.POST.get("number_of_rooms")
        request_data["bed_per_room"] = request.POST.get("bed_per_room")
        request_data["price"] = request.POST.get("price")
        request_data["created_by"] = request.user
        # request_data["hostel"] = hostel
        if hostel.create_roomtype(request_data):
            return reverse_lazy("my-hostel-roomtypes")
        else:
            return render(request, "housing/roomtypes/create-roomtype.html", context)
    else:
        return render(request, "housing/roomtypes/create-roomtype.html", context)


def create_room(request, slugname):
    hostel = get_object_or_404(klass=housing_models.Hostels, nameslug=slugname)
    context = {"hostel": hostel}
    if request.method == "POST":
        room_type = request.POST.get("bedtype")
        num_rooms = request.POST.get("num_of_rooms")
        # generate_rooms(room_type=room_type, num_rooms=num_rooms, hostel=hostel)
    else:
        return render(request, "housing/rooms/create_room.html", context)


def search_hostel(request):
    hostels = housing_models.Hostels.objects.all()
    min_budget = request.GET.get("min-budget")
    max_budget = request.GET.get("max-budget")
    neighborhood = request.GET.get("neighborhood")
    name = request.GET.get("name")
    city = request.GET.get("city")
    amenities = request.GET.get("amenities")
    roomtypes = request.GET.get("roomtypes")
    if name:
        hostels = hostels.filter(name__icontains=name)
    if city:
        hostels = hostels.filter(city__id=city)
    if neighborhood:
        hostels = hostels.filter(neighborhood__id=neighborhood)
    if roomtypes:
        roomtype_filters = Q()
        for roomtype_id in roomtypes.split("||"):
            try:
                uuid_roomtype = UUID(roomtype_id)
                roomtype_filters |= Q(room_types__id=uuid_roomtype)
            except ValueError:
                return HttpResponseBadRequest("Invalid UUID in roomtypes list")
        hostels = hostels.filter(roomtype_filters)
    # print(hostels)
    if amenities:
        amenity_filters = Q()
        for amenity_id in amenities.split("||"):
            try:
                uuid_amenity = UUID(amenity_id)
                amenity_filters |= Q(amenities__id=uuid_amenity)
            except ValueError:
                return HttpResponseBadRequest("Invalid UUID in amenities list")
        hostels = hostels.filter(amenity_filters)
    cities = hms_models.City.objects.all()
    neighborhoods = hms_models.Neighborhoods.objects.all()
    roomtypes = housing_models.RoomTypes.objects.all().order_by("room_type_code")
    amenities = housing_models.Amenities.objects.all()[:20]
    context = {
        "hostels": hostels,
        "cities": cities,
        "roomtypes": roomtypes,
        "amenities": amenities,
        "neighborhoods": neighborhoods,
    }
    if request.GET:
        return render(request, "housing/hostels/search-results.html", context)
    return render(request, "housing/hostels/search-hostel.html", context)


def submit_application(request):
    # room_types = housing_models.HostelRoomTypes.objects.filter(
    #     hostel=request.user.hostel
    # )
    room_types = housing_models.HostelRoomTypes.objects.all(
        # hostel=request.user.hostel
    )
    payload = {}
    refine_payload = {}
    room_types_string = ""
    for room_type in room_types:
        room_types_string += f"{room_type.id}||{room_type}~~"
    context = {"room_types": room_types, "room_types_string": room_types_string}
    if request.method == "POST":
        roomtypes = {}
        for key, value in request.POST.items():
            # print(key, value)
            if key == "csrfmiddlewaretoken":
                continue
            if key.startswith("hostel_"):
                refine_payload[key] = value
            elif key.startswith("roomtype_"):
                hostel_id = key.split("_")[1]
                roomtypes[hostel_id] = value
            else:
                payload[key] = value
        hostels = [
            k.split("_")[1]
            for k, v in refine_payload.items()
            if k.split("_")[0] == "hostel" and k != "csrfmiddlewaretoken"
        ]
        code = str(uuid.uuid4()).split("-")[0]
        try:
            application = housing_models.Application.objects.create(
                code=code, **payload
            )
            # application = housing_models.A
            for hostel_id in hostels:
                hostel = housing_models.Hostels.objects.get(id=hostel_id)
                room_type = housing_models.HostelRoomTypes.objects.get(
                    id=roomtypes[hostel_id]
                )
                housing_models.ApplicationHostel.objects.create(
                    application=application,
                    hostel=hostel,
                    room_type=room_type,
                    code=application.code,
                    status=default_application_status,
                )
            send_mail(
                subject="Application sent successfully.",
                message="Hello, your application has been sent to the selected hostels.",
                from_email="groupfiftyeight95@gmail.com",
                recipient_list=[application.applicant_email],
                fail_silently=False
            )
            return redirect(
                reverse_lazy(
                    "application-sent", kwargs={"application_code": application.code}
                )
            )
        except Exception as e:
            print(f"an error occured while creating application: {e}")
            return render(request, "housing/hostels/application-form.html", context)
    return render(request, "housing/hostels/application-form.html", context)


def application_sent(request):
    context = {}
    return render(request, "housing/hostels/application-sent.html", context)


def find_application(request):
    application_code = request.GET.get("application-code")
    print(type(application_code))
    context = {"application_code": application_code}
    application = housing_models.Application.objects.get(code=application_code)
    context["application"] = application
    return render(request, "housing/hostels/application-details.html", context)


# TODO: only accessible by hostel admins, after they have created their profiles or assigned role to make offers
def make_housing_offer(request, application_id):
    hostel = request.user.hostel
    application_id = UUID(application_id)
    application_hostel = get_object_or_404(
        housing_models.ApplicationHostel, application__id=application_id, hostel=hostel
    )
    room_type = application_hostel.room_type

    rooms = housing_models.Rooms.objects.filter(
        hostel=hostel, room_type=application_hostel.room_type
    )
    context = {"application_hostel": application_hostel, "rooms": rooms}
    if request.method == "POST":
        room = request.POST.get("offered-room")
        offer_date = request.POST.get("offer-date")
        comment = request.POST.get("offer-comment")
        try:
            room = get_object_or_404(housing_models.Rooms, id=UUID(room))
            hostel_offer = housing_models.HousingOffer.objects.create(
                hostel=hostel,
                application_hostel=application_hostel,
                room=room,
                room_type=room.room_type,
                applicant_name=application_hostel.application.tenant_name,
                email=application_hostel.application.email,
                phone=application_hostel.application.phone,
                date_offered=offer_date,
                comment=comment,
                offered_by=request.user,
                status=default_application_status,
            )
            print(hostel_offer)
            messages.success(
                request,
                _(
                    f"You have made an offer to {application_hostel.application.tenant_name}. Application ID: {application_hostel.application.code}"
                ),
            )
            return redirect(reverse_lazy("my-applications"))
        except Exception as e:
            print(f"An error occured {e}")
    return render(request, "housing/hostels/create-hostel-offer.html", context)


def search_application(request):
    application_code = request.GET.get("application-code")
    context = {}
    try:
        application = housing_models.Application.objects.get(code=application_code)
        context["application"] = application
        return render(request, "housing/hostels/search-application.html", context)
    except ObjectDoesNotExist as e:
        messages.error(
            request,
            _(
                f"No application exists with the given code. Kindly check the code and search again"
            ),
        )
        return render(request, "housing/hostels/search-application.html")


def housing_offer_details(request, application_code):
    housing_offer = get_object_or_404(housing_models.HousingOffer, application_hostel__)
