from typing import Any
from django import forms
from .models import (
    Tenant, Hostel, Address, Block, 
    Room, TenantRoomAssignment, HostelVendor,
    RoomRequest
)
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError

class TenantCreationForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ["user", "email"]

    
class HostelCreationForm(forms.ModelForm):
    class Meta:
        model = Hostel
        exclude = [
            "warden", "created_by", 
            "amenities", "status", "vendor"
        ]

class HostelAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["hostel"]

class BlockCreationForm(forms.ModelForm):
    class Meta:
        model = Block
        exclude = ["hostel"]

class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ["hostel"]

class RoomAssignmentForm(forms.ModelForm):
    class Meta:
        model = TenantRoomAssignment
        fields = ["tenant", "room", "start_date", "end_date"]

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        if room:
            room_capacity = room.capacity
            current_assignment_count = room.tenantroomassignment_set.filter(
                Q(end_date__isnull=True) | Q(end_date__gt=timezone.now())
            ).count()
            if current_assignment_count >= room_capacity:
                raise ValidationError("Room capacity exceeded. Cannot assign more tenants to this room")
            
        return cleaned_data
    
class HostelVendorCreationForm(forms.ModelForm):
    class Meta:
        model = HostelVendor
        exclude = [
            "created_by",
            "payment_details", "is_verified", "description",
        ]

class RoomRequestCreationForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        exclude = [
            "date_created", "last_modified", 
            "request_status"
        ]