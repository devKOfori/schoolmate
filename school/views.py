from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_list_or_404, get_object_or_404
from housing import models as housing_models
from employee import models as emp_models

# Create your views here.

def dashboard(request):
    user = request.user
    
    context = {
        'hide_menu': True,
        'dashboard_nav': True,
    }
    return render(request, 'school/dashboard.html', context)
    
def index(request):
    return render(request, "school/index.html")