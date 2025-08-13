from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    
    # Authentication pages
    path('hr_login/', views.hr_login, name='hr_login'),
    path('employee_login/', views.employee_login, name='employee_login'),
    
    # Dashboard and home pages
    path('hr_home/', views.hr_home, name='hr_home'),
    path('employee_home/', views.employee_home, name='employee_home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ceo_dashboard/', views.ceo_dashboard, name='ceo_dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('transaction/', views.transaction, name='transaction'),
    path('logout/', views.logout_view, name='logout'),
    path('logout_all/', views.logout_all, name='logout_all'),
    path('clear_session/', views.clear_session, name='clear_session'),
    path('document/', views.document, name='document'),
    
    # API endpoints
    path('api/financial_data/', views.api_financial_data, name='api_financial_data'),
]