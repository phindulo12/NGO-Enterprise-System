from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)  # test line
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = user.role  # Assuming role is a field on CustomUser
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'project_manager':
                return redirect('project_manager_dashboard')
            elif role == 'accountant':
                return redirect('accountant_dashboard')
            elif role == 'reporter':
                return redirect('reporter_dashboard')
            else:
                return redirect('staff_dashboard')
        else:
            error = "Invalid username or password"
    return render(request, 'accounts/login.html', {'error': error})
def logout_view(request):
    logout(request)
    return redirect('login')
# Create your views here.
