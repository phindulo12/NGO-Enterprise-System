"""
URL configuration for ngo_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (home,project_manager_dashboard,accountant_dashboard,reporter_dashboard,staff_dashboard,)
from django.urls import path, include

from . import views


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('dashboard/project-manager/',views.project_manager_dashboard, name = 'project_manager_dashboard' ),
    path('dashboard/accountant/',views.accountant_dashboard, name = 'accountant_dashboard' ),
    path('dashboard/reporter/',views.reporter_dashboard, name = 'reporter_dashboard' ),
    path('accounts/', include('accounts.urls')),
    path('dashboard/staff/',views.staff_dashboard, name = 'staff_dashboard' )
]