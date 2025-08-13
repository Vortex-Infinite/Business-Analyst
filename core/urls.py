from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main pages
    path('', views.index_view, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('analytics/', views.analytics_view, name='analytics'),
    
    # Authentication
    path('hr_login/', views.hr_login_view, name='hr_login'),
    path('employee_login/', views.employee_login_view, name='employee_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # API endpoints
    path('api/financial-data/', views.api_financial_data, name='api_financial_data'),
    path('api/dashboard-metrics/', views.api_dashboard_metrics, name='api_dashboard_metrics'),
]
