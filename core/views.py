from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Renders the main portal page
def index(request):
    return render(request, 'index.html')

# Renders the HR login page
def hr_login(request):
    return render(request, 'hr_login.html')

# Renders the Employee login page
def employee_login(request):
    return render(request, 'employee_login.html')

# Renders the HR dashboard
def hr_dashboard(request):
    return render(request, 'dashboard.html')

# Renders the Employee dashboard
def employee_dashboard(request):
    return render(request, 'employee_home.html')

# Renders the HR home page
def hr_home(request):
    return render(request, 'hr_home.html')

# Renders the Employee home page
def employee_home(request):
    return render(request, 'employee_home.html')

# Renders the dashboard page
def dashboard(request):
    return render(request, 'dashboard.html')

# Renders the CEO dashboard page
def ceo_dashboard(request):
    return render(request, 'ceo_dashboard.html')

# Renders the document page
def document(request):
    return render(request, 'document.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')