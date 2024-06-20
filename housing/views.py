import datetime
import uuid
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
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
    RoomRequest, VerifyProperty, RoomCategory
)
from employee import models as employee_models
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from school import models as schmodels
from django.views import generic
# Create your views here.
import utils
from django.utils import timezone
from accounts import models as account_models

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














class HostelCreateView(LoginRequiredMixin, generic.CreateView):
    model = Hostel
    form_class = HostelCreationForm
    template_name = 'housing/create_hostel.html'

    def get_initial(self):
        initials = super().get_initial()
        initials['hostel_id'] = utils.generate_hostel_id()
        return initials

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # initials = self.get_initial()
        # hostel_id = initials.get('hostel_id')
        # context['hostel_id'] = hostel_id
        return context
    
    def form_valid(self, form):
        cleaned_data =  form.cleaned_data
        logged_in_user = self.request.user
        print(logged_in_user)
        form.instance.company = cleaned_data.get('name', '')
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        form = HostelCreationForm(request.POST)
        # change this. set default value (utils.generate_hostel_id) on hostel_id field of Hostel Model
        if not request.POST.get('hostel_id'):
            form.data['hostel_id'] = utils.generate_hostel_id()
        print(f"***Hostel ID: {request.POST.get('hostel_id')}")
        if form.is_valid():
            print("I am here")
            hostel = form.save(commit=False)
            hostel.created_by = request.user
            hostel.save()
            return redirect(reverse("hostel-detail", kwargs={"hostel_id": hostel.hostel_id}))
        print(form.errors)
        return render(request, "housing/create_hostel.html")
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print('I got here')
        return super().form_invalid(form)







































def hostel_detail(request, hostel_id):
    hostel_application_form = forms.HostelApplicationForm
    hostel = get_object_or_404(Hostel, hostel_id=hostel_id)
    hostel_rooms = Room.objects.filter(hostel=hostel)
    hostel_items = models.Facility.objects.filter(hostel = hostel)
    context = {
        "hostel": hostel,
        "rooms": hostel_rooms,
        "items": hostel_items,
        "hostel_application_form": hostel_application_form
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
    cities = schmodels.City.objects.all()
    print(cities)
    hostels = Hostel.objects.all()
    context = {
        "hostels": hostels,
        "cities": cities
    }
    return render(request, "housing/hostel_list.html", context=context)

def search(request):
    hostels = Hostel.objects.all()
    cities = schmodels.City.objects.all()
    hostel_name = request.GET.get("hostel_name")
    room_category = request.GET.get("room_category")
    city = request.GET.get("city")
    if hostel_name:
        hostels = hostels.filter(name__icontains=hostel_name)
    if room_category:
        # print(room_category)
        hostels = hostels.filter(room__room_category__name=room_category).distinct()
    if city:
        hostels = hostels.filter(hosteladdress__city__name=city)
    context = {
        "hostels": hostels,
        "cities": cities
    }
    return render(request, "housing/hostel_list.html", context=context)

class SearchListView(generic.ListView):
    model = models.Hostel
    context_object_name = "hostels"
    template_name = "housing/search_hostel.html"

    def get_queryset(self):
        room_category_name = self.kwargs.get('room_category').title()
        if room_category_name and room_category_name in ['Shared', 'Single']:
            room_category = RoomCategory.objects.filter(name=room_category_name).first()

            if room_category:
                queryset = Hostel.objects.filter(room__room_category=room_category).distinct()
            else:
                queryset = Hostel.objects.none()  # Return an empty queryset if the category doesn't exist
        else:
            queryset = Hostel.objects.all()
        location = self.request.GET.get('location', None)
        rc = self.request.GET.get('roomcategory', None)
        # print(location)
        if location:
            queryset = queryset.filter(location=location)
        if rc:
            if rc != 'All':
                queryset = queryset.filter(room__room_category__name=rc)
            print(queryset)
        return queryset.distinct()   
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hostel_count = self.get_queryset().count()
        context['hostel_count'] = hostel_count
        return context
    
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

class MyHostelRoomListView(generic.ListView):
    model = Room
    context_object_name = "rooms"
    template_name = "housing/room_list.html"

    def get_queryset(self):
        employee = self.request.user.employee
        emp_hostel_alloc = models.HostelEmployeeAlloc.objects.filter(
            employee=employee
        ).last()
        queryset =  super().get_queryset()
        queryset.filter(
            hostel = emp_hostel_alloc.hostel
        )
        return queryset
    
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
         
class HostelEmployeeAllocCreateView(generic.CreateView):
    model = models.HostelEmployeeAlloc
    form_class = HostelEmployeeAllocForm
    template_name = "housing/assign_new_role.html"
    success_url = reverse_lazy("my-employee")

    def form_valid(self, form):
        logged_in_emp = self.request.user.employee
        logged_in_emp_hostel_alloc = models.HostelEmployeeAlloc.objects.filter(
            employee = logged_in_emp
        ).last()
        print(logged_in_emp_hostel_alloc)
        logged_in_emp_hostel = logged_in_emp_hostel_alloc.hostel

        employee_id = self.request.POST.get("upd_employee_id")
        form_type = self.request.POST.get("form_type")
        # if form_type:
        setattr(form.instance, "upd_employee_id", employee_id)
        setattr(form.instance, "upd_added_by", self.request.user.employee)
        setattr(form.instance, "upd_hostel", logged_in_emp_hostel)
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


class RoomTypeCreateView(generic.CreateView):
    model = models.RoomType
    form_class = forms.RoomTypeForm
    template_name = "housing/create_room_type.html"
    # success_url = reverse_lazy("my-employee")

    def form_valid(self, form):
        employee = self.request.user.employee
        assigned_hostel = models.HostelEmployeeAlloc.objects.filter(
            employee = employee
        ).last()
        form.instance.hostel = assigned_hostel.hostel
        create_rooms = self.request.POST.get("create_rooms")
        if create_rooms:
            setattr(form.instance, "create_rooms", True)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        frm_add_another = self.request.POST.get("add_another")
        if frm_add_another:
            return reverse("create-roomtype")
        return reverse("my-employee")

class RoomCreateView(generic.CreateView):
    model = Room
    template_name = "housing/create_room.html"
    form_class = forms.RoomForm
    
    def get_success_url(self) -> str:
        return reverse_lazy("room-detail", kwargs={"room_number": self.object.room_number})
    
    def form_valid(self, form):
        employee = self.request.user.employee
        emp_hostel_alloc = models.HostelEmployeeAlloc.objects.filter(
            employee=employee
        ).last()
        assigned_hostel = emp_hostel_alloc.hostel
        form.instance.hostel = assigned_hostel
        form.instance.created_at = datetime.datetime.now()
        form.instance.created_by = self.request.user.employee
        return super().form_valid(form)
    
    def get_initial(self):
        last_room = Room.objects.last()
        last_id = int(last_room.room_number[2:])
        new_id = last_id + 1
        new_room_number = "RM" + str(new_id).zfill(7)
        initial = super().get_initial()
        initial["room_number"] = new_room_number
        return initial
    
class HostelItemListView(generic.ListView):
    model = models.Facility
    context_object_name = "hostel_items"
    template_name = "housing/list_hostel_items.html"

    def get_queryset(self):
        employee = self.request.user.employee
        emp_hostel_alloc = models.HostelEmployeeAlloc.objects.filter(
            employee = employee
        ).last()
        queryset = super().get_queryset()
        queryset.filter(hostel = emp_hostel_alloc.hostel)
        return queryset

class HostelItemCreateView(generic.CreateView):
    model = models.Facility
    form_class = forms.HostelItemForm
    template_name = "housing/create_hostel_item.html"
    # success_url = reverse("room-detail")

    def form_valid(self, form):
        employee = self.request.user.employee
        hostel_id = self.kwargs.get("hostel_id")
        if hostel_id:
            hostel = Hostel.objects.get(hostel_id = hostel_id)
        form.instance.hostel = hostel
        form.instance.added_by = employee
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        hostel_id = self.kwargs.get("hostel_id")
        frm_add_another = self.request.POST.get("add_another")
        if frm_add_another:
            return reverse("create-hostel-item", kwargs={"hostel_id": hostel_id})
        return reverse("list-hostel-items", kwargs={"hostel_id": hostel_id})
    
class TenantCreateView(generic.CreateView):
    model = models.HostelTenant
    form_class = forms.TenantForm
    template_name = "housing/register_tenant.html"
    success_url = reverse_lazy("my-hostels")

    def form_valid(self, form):
        active_user = self.request.user.employee
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        password = form.cleaned_data.get("password")
        user = account_models.CustomUser.objects.create_user(
            first_name=first_name, last_name=last_name, 
            email=email, username=email, password=password, 
            is_superuser=False, is_staff=False
        )
        form.instance.user = user
        form.instance.created_by = active_user
        form.instance.created_at = datetime.datetime.now()
        return super().form_valid(form)
    
class TenantListView(generic.ListView):
    model = models.HostelTenant
    context_object_name = "tenants"
    template_name = "housing/list_tenants.html"

class HostelApplicationCreateView(generic.CreateView):
    model = models.HostelApplication
    form_class = forms.HostelApplicationForm
    template_name = "housing/hostel_application.html"
    # success_url = reverse_lazy("hostel-application-detail")

    def form_valid(self, form):
        hostel_application = form.save()
        hostels = form.cleaned_data.get("hostels")
        rooms = form.cleaned_data.get("rooms")
        room_types = form.cleaned_data.get("room_types")
        if hostels:
            hostel_application.hostels.set(hostels)
        if rooms:
            hostel_application.rooms.set(rooms)
        if room_types:
            hostel_application.room_types.set(room_types)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        application_id = self.object.application_id
        return reverse_lazy("hostel-application-detail", kwargs={"application_id": application_id})

class HostelApplicationDetailView(generic.DetailView):
    model = models.HostelApplication
    context_object_name = "hostelapplication"
    template_name = "housing/hostel_application_detail.html"
    slug_field = "application_id"