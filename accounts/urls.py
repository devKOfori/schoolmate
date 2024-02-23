from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]