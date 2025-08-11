from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render

# Renders the main portal page
def index(request):
    return render(request, 'index.html')

# Renders the HR login page
def hr_login(request):
    return render(request, 'hr_login.html')

# Renders the Employee login page
def employee_login(request):
    return render(request, 'employee_login.html')

# Renders the HR home page
def hr_home(request):
    return render(request, 'hr_home.html')

# Renders the Employee home page
def employee_home(request):
    return render(request, 'employee_home.html')

# Renders the dashboard
def dashboard(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('hr_login')
def document(request):
    return render(request, 'document.html')