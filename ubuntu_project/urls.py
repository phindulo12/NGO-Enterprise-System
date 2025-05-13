from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.ubuntu_dashboard, name='ubuntu_dashboard'),
]
