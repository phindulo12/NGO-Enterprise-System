from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the NGO Enterprise System!")

def project_manager_dashboard(request):
    return HttpResponse("Welcome, Project Manager!")


def accountant_dashboard(request):
    return HttpResponse("Welcome, Accountant!")


def reporter_dashboard(request):
    return HttpResponse("Welcome, Reporter!")


def staff_dashboard(request):
    return HttpResponse("Welcome, NGO Staff!")


