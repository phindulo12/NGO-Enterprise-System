from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.shortcuts import render

@login_required
@role_required(allowed_roles=['admin'])
def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')

@login_required
@role_required(allowed_roles=['project_manager'])
def project_manager_dashboard(request):
    return render(request, 'dashboards/project_manager_dashboard.html')

@login_required
@role_required(allowed_roles=['accountant'])
def accountant_dashboard(request):
    return render(request, 'dashboards/accountant_dashboard.html')

@login_required
@role_required(allowed_roles=['reporter'])
def reporter_dashboard(request):
    return render(request, 'dashboards/reporter_dashboard.html')

@login_required
@role_required(allowed_roles=['staff'])
def staff_dashboard(request):
    return render(request, 'dashboards/staff_dashboard.html')

