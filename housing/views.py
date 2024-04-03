import datetime
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import (
    TenantCreationForm, HostelCreationForm, HostelAddressForm,
    BlockCreationForm, RoomCreationForm, RoomAssignmentForm,
    HostelVendorCreationForm, RoomRequestCreationForm, 
    VerifyPropertyForm, UpdateDocumentVerificationForm,
    HostelEmployeeAllocForm
)
from . import forms
from . import models
from accounts.forms import (
    UserCreationForm
)
from .models import (
    HostelStatus, Hostel, Room, HostelVendor,
    RoomRequest, VerifyProperty
)
from employee import models as employee_models
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.views import generic
# Create your views here.
import utils
from django.utils import timezone
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

#======================================================================================================================
#               VENDOR VIEWS
#======================================================================================================================

def setup_vendor(request):
    vendor_form = HostelVendorCreationForm()
    employee = request.user.employee
    if request.method == "POST":
        vendor_form = HostelVendorCreationForm(request.POST)
        if vendor_form.is_valid():
            vendor = vendor_form.save(commit=False)
            vendor.created_by = employee
            vendor.save()
            return redirect(reverse("vendor-detail", kwargs={"vendor_id":vendor.vendor_id}))
        return render(request, "housing/create_vendor.html", {"vendor_form":vendor_form})
    else:
        return render(request, "housing/create_vendor.html", {"vendor_form":vendor_form})
    
def all_vendors(request):
    vendors = HostelVendor.objects.all()
    context = {
        "vendors": vendors
    }
    return render(request, "housing/vendor_list.html", context)

def my_vendors(request):
    me = request.user.employee
    vendors = HostelVendor.objects.filter(created_by=me)
    context = {
        "vendors": vendors
    }
    return render(request, "housing/vendor_list.html", context)

def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(HostelVendor, vendor_id=vendor_id)
    return render(request, "housing/vendor_detail.html", {"vendor":vendor})

#======================================================================================================================
#               HOSTEL VIEWS
#======================================================================================================================

def create_hostel(request):
    company_code = request.user.employee.company_code
    vendor = HostelVendor.objects.get(vendor_id=company_code)
    hostel_form = HostelCreationForm(prefix="hostel")
    hostel_address_form = HostelAddressForm(prefix="address")
    default_hostel_status = HostelStatus.objects.first()
    if request.method == "POST":
        hostel_form = HostelCreationForm(request.POST, prefix="hostel")
        hostel_address_form = HostelAddressForm(request.POST, prefix="address")
        if hostel_form.is_valid() and hostel_address_form.is_valid():
            hostel = hostel_form.save(commit=False)
            hostel.created_by = request.user.employee
            # hostel.warden = request.user
            hostel.vendor = vendor
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

def my_hostels(request):
    me = request.user.employee
    my_vendor = HostelVendor.objects.get(vendor_id=me.company_code)
    hostels = Hostel.objects.filter(vendor=my_vendor)
    context = {
        "hostels": hostels
    }
    return render(request, "housing/hostel_list.html", context=context)

def hostel_list(request):
    hostels = Hostel.objects.all()
    context = {
        "hostels": hostels
    }
    return render(request, "housing/hostel_list.html", context=context)


#======================================================================================================================
#               PROFILE VERIFICATION
#======================================================================================================================
def verify_property(request, property_id):
    verify_property_form = VerifyPropertyForm()
    if request.method == "POST":
        verify_property_form = VerifyPropertyForm(request.POST, request.FILES)
        if verify_property_form.is_valid():
            verify_property = verify_property_form.save(commit=False)
            verify_property.application_id = property_id
            verify_property.upload_by = request.user.employee
            verify_property.valid = True
            verify_property.save()
            if verify_property.property_type.name.upper() == "HOSTEL":
                return redirect(reverse("hostel-detail", kwargs={"hostel_id": property_id}))
            return redirect(reverse("vendor-detail", kwargs={"vendor_id": property_id}))
        return render(request, "housing/upload_verification_document.html", {"verify_property_form": verify_property_form})
    else:
        return render(request, "housing/upload_verification_document.html", {"verify_property_form": verify_property_form})

class UpdateDocumentVerificationCreateView(generic.CreateView):
    model = models.DocumentVerificationPro
    form_class = forms.UpdateDocumentVerificationForm
    template_name = "housing/create_update_document_verification.html"
    success_url = reverse_lazy("list-property-verification")

    def form_valid(self, form, *args, **kwargs):
        property_id = self.kwargs.get("property_id")
        verify_property = get_object_or_404(VerifyProperty, application_id=property_id)
        # filter = Q(application_id=property_id) & Q(property_type=form.instance.verify_property)
        doc_ver_pro = models.DocumentVerificationPro.objects.filter(verify_property=verify_property).last()
        if doc_ver_pro:
            doc_ver_pro.valid = False
            doc_ver_pro.save()
        form.instance.verify_property = verify_property
        form.instance.updatedocumentverification_id = property_id + "_" + str(datetime.datetime.now())
        form.instance.date_of_update = datetime.datetime.today()
        form.instance.updated_by = self.request.user.employee
        form.instance.last_update_message = f"The update is done by employee ID: {self.request.user.employee.employee_id}, employee Name: {self.request.user.employee} on {str(datetime.datetime.now())}"
        form.instance.comment = ""
        return super().form_valid(form)

  
class DocumentVerificationListView(generic.ListView):
    model = VerifyProperty
    template_name = "housing/document_verification_list.html"
    context_object_name = "documentverifications"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_form = UpdateDocumentVerificationForm()
        context["update_form"] = update_form
        return context

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

def request_room(request):
    room_request_form = RoomRequestCreationForm()
    if request.method == "POST":
        room_request_form = RoomRequestCreationForm(request.POST)
        if room_request_form.is_valid():
            room_request = room_request_form.save()
            return redirect(reverse("dashboard"))
        return render(request, "housing/room_request.html", {"room_request_form":room_request_form})
    else:
        return render(request, "housing/room_request.html", {"room_request_form":room_request_form})
    
def all_room_requests(request):
    room_requests = RoomRequest.objects.all()
    context = {
        "room_requests": room_requests
    }
    return render(request, "housing/room_request_list.html", context)

def my_hostel_requests(request):
    hostel_manager = request.user.employee
    managed_rooms = Room.objects.filter(
        Q(hostel__created_by=hostel_manager) |
        Q(created_by=hostel_manager)
    )
    print(managed_rooms.values_list("hostel__hostel_id", flat=True))  
        # Get all room requests that match the criteria
    room_requests = RoomRequest.objects.filter(
        preferred_hostels__hostel_id__in=managed_rooms.values_list('hostel__hostel_id', flat=True)
    )
    context = {
        "room_requests": room_requests
    }
    return render(request, "housing/room_request_list.html", context)
         
# def room_request_detail(request, request_id):
#     room_request = get_object_or_404(RoomRequest, request_id=request_id)
#     preferences = room_request.get_preferences()
#     prefered_hostels = preferences.get("hostels")
#     prefered_amenities = preferences.get("amenities")
#     prefered_room_types = preferences.get("room_types")
#     prefered_facilities = preferences.get("facilities")
#     number_of_beds = preferences.get("number_of_beds")
#     min_budget = preferences.get("min_budget")
#     max_budget = preferences.get("max_budget")
#     duration_of_stay = preferences.get("duration_of_stay")
#     move_in_date_earliest = preferences.get("move_in_date_earliest")
#     move_in_date_latest = preferences.get("move_in_date_latest")

#     preferrence_filters = Q()
#     hostels_filter = Q()

#     if prefered_hostels:
#         hostels = Hostel.objects.filter(name__in=prefered_hostels)
#         hostel_rooms = Room.objects.filter(Q(hostel__in=hostels))
#         hostels_filter &= Q(preferred_hostels__name__in=prefered_hostels)
#     if prefered_amenities:
#         preferrence_filters &= Q(preferred_amenities__name__in=prefered_amenities)
#     if prefered_room_types:
#         preferrence_filters &= Q(preferred_room_types__name__in=prefered_room_types)
#     if prefered_facilities:
#         preferrence_filters &= Q(preferred_facilities__name__in=prefered_facilities)
#     if number_of_beds:
#         preferrence_filters &= Q(number_of_beds_required=number_of_beds)
#     if min_budget:
#         preferrence_filters &= Q(min_budget=min_budget)
#     if max_budget:
#         preferrence_filters &= Q(max_budget=max_budget)
#     if duration_of_stay:
#         preferrence_filters &= Q(duration_of_stay=duration_of_stay)
#     if move_in_date_earliest:
#         preferrence_filters &= Q(move_in_date_earliest=move_in_date_earliest)
#     if move_in_date_latest:
#         preferrence_filters &= Q(move_in_date_latest=move_in_date_latest)
    
#     available_rooms = Room.objects.filter(preferrence_filters)
    
#     context = {
#         "room_request": room_request, 
#         "available_rooms": available_rooms
#     }
#     return render(request, "housing/room_request_detail.html", context)

class HostelEmployeeAllocCreateView(generic.CreateView):
    model = models.HostelEmployeeAlloc
    form_class = HostelEmployeeAllocForm
    template_name = "housing/assign_new_role.html"
    success_url = reverse_lazy("my-employee")

    def form_valid(self, form):
        employee_id = self.request.POST.get("upd_employee_id")
        form_type = self.request.POST.get("form_type")
        # if form_type:
        setattr(form.instance, "upd_employee_id", employee_id)
        setattr(form.instance, "upd_added_by", self.request.user.employee)
        return super().form_valid(form)


def update_employee_role(request):
    added_by = request.user.employee
    emp_id = request.POST.get("employee_id")
    print(emp_id)
    if request.method == "POST":
        emp_hostel_alloc_form = HostelEmployeeAllocForm(request.POST)
        if emp_hostel_alloc_form.is_valid():
            role = emp_hostel_alloc_form.cleaned_data.get("role")
            if added_by and emp_id:
                emp = models.Employee.objects.get(employee_id=emp_id)
                emp_hostel_alloc = models.HostelEmployeeAlloc.objects.filter(employee=emp).last()
                utils.deactivate_role(emp_hostel_alloc)
                new_role = models.HostelEmployeeAlloc(
                    hostel=emp_hostel_alloc.hostel,
                    employee=emp,
                    role = role,
                    active = True,
                    added_by = added_by,
                    timestamp = timezone.now(),
                    comment = ""
                )
                new_role.save()
                utils.update_emp_info(emp, emp_hostel_alloc.hostel.hostel_id)
