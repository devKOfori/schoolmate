from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('signup/', views.register_user, name='register'),
    path('logout/', views.user_logout, name='logout'),
]