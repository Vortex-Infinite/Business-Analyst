from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Avg, Max, Min, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import DailyFinancialData, Company, QuarterlySummary, UserProfile

def index(request):
    """Enhanced landing page with real data preview"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Get latest company data for preview
    try:
        company = Company.objects.first()
        latest_data = DailyFinancialData.objects.filter(company=company).first()
        
        context = {
            'company': company,
            'latest_revenue': latest_data.revenue if latest_data else 0,
            'latest_profit': latest_data.profit if latest_data else 0,
            'latest_profit_margin': latest_data.profit_margin if latest_data else 0,
            'last_updated': latest_data.date if latest_data else None,
        }
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'index.html', context)

def hr_login(request):
    """HR login with authentication"""
    if request.method == 'POST':
        username = request.POST.get('hrId')
        password = request.POST.get('hrPassword')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('ceo_dashboard')
        else:
            return render(request, 'hr_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'hr_login.html')

def employee_login(request):
    """Employee login with authentication"""
    if request.method == 'POST':
        username = request.POST.get('employeeId')
        password = request.POST.get('employeePassword')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'employee_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'employee_login.html')

@login_required
def dashboard(request):
    """Updated business analyst dashboard with financial metrics"""
    company = Company.objects.first()
    
    if not company:
        return render(request, 'dashboard.html', {'error': 'No company data found. Please import financial data first.'})
    
    # Get recent data for analysis
    recent_data = DailyFinancialData.objects.filter(company=company)[:30]
    
    # Performance metrics for last 90 days
    ninety_days_ago = timezone.now().date() - timedelta(days=90)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    sixty_days_ago = timezone.now().date() - timedelta(days=60)
    
    # Current period stats
    current_stats = DailyFinancialData.objects.filter(
        company=company,
        date__gte=thirty_days_ago
    ).aggregate(
        total_revenue=Sum('revenue'),
        total_expenditure=Sum('expenditure'),
        actual_profit=Sum('profit'),
        avg_profit_margin=Avg('profit_margin'),
        max_revenue=Max('revenue'),
        min_revenue=Min('revenue')
    )
    
    # Previous period stats for comparison
    previous_stats = DailyFinancialData.objects.filter(
        company=company,
        date__gte=sixty_days_ago,
        date__lt=thirty_days_ago
    ).aggregate(
        total_revenue=Sum('revenue'),
        total_expenditure=Sum('expenditure'),
        actual_profit=Sum('profit'),
        avg_profit_margin=Avg('profit_margin')
    )
    
    # Calculate trends
    revenue_trend = 0
    expense_trend = 0
    profit_trend = 0
    margin_trend = 0
    
    if previous_stats['total_revenue'] and current_stats['total_revenue']:
        revenue_trend = ((current_stats['total_revenue'] - previous_stats['total_revenue']) / previous_stats['total_revenue']) * 100
    
    if previous_stats['total_expenditure'] and current_stats['total_expenditure']:
        expense_trend = ((current_stats['total_expenditure'] - previous_stats['total_expenditure']) / previous_stats['total_expenditure']) * 100
    
    if previous_stats['actual_profit'] and current_stats['actual_profit']:
        profit_trend = ((current_stats['actual_profit'] - previous_stats['actual_profit']) / previous_stats['actual_profit']) * 100
    
    if previous_stats['avg_profit_margin'] and current_stats['avg_profit_margin']:
        margin_trend = current_stats['avg_profit_margin'] - previous_stats['avg_profit_margin']
    
    # Enhanced performance stats
    performance_stats = {
        'total_revenue': current_stats['total_revenue'] or 0,
        'total_expenditure': current_stats['total_expenditure'] or 0,
        'actual_profit': current_stats['actual_profit'] or 0,
        'avg_profit_margin': current_stats['avg_profit_margin'] or 0,
        'max_revenue': current_stats['max_revenue'] or 0,
        'min_revenue': current_stats['min_revenue'] or 0,
        'revenue_trend': round(revenue_trend, 1) if revenue_trend else 0,
        'expense_trend': round(expense_trend, 1) if expense_trend else 0,
        'profit_trend': round(profit_trend, 1) if profit_trend else 0,
        'margin_trend': round(margin_trend, 1) if margin_trend else 0,
        'monthly_revenue': current_stats['total_revenue'] or 0,
        'monthly_expenses': current_stats['total_expenditure'] or 0,
        'monthly_profit': current_stats['actual_profit'] or 0,
        'roi': round((current_stats['actual_profit'] / current_stats['total_expenditure'] * 100), 1) if current_stats['total_expenditure'] else 0
    }
    
    # Trend data for charts (last 10 days)
    trend_data = []
    for data in recent_data[:10]:
        trend_data.append({
            'date': data.date.strftime('%Y-%m-%d'),
            'revenue': float(data.revenue),
            'expenditure': float(data.expenditure),
            'profit': float(data.profit),
            'profit_margin': float(data.profit_margin)
        })
    
    context = {
        'company': company,
        'recent_data': recent_data,
        'performance_stats': performance_stats,
        'trend_data': json.dumps(trend_data[::-1]),  # Reverse for chronological order
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def ceo_dashboard(request):
    """CEO dashboard with comprehensive analytics"""
    company = Company.objects.first()
    
    if not company:
        return render(request, 'ceo_dashboard.html', {'error': 'No company data found. Please import financial data first.'})
    
    # Get current year data
    current_year = timezone.now().year
    current_year_data = DailyFinancialData.objects.filter(company=company, year=current_year)
    previous_year_data = DailyFinancialData.objects.filter(company=company, year=current_year - 1)
    
    # Calculate year-over-year metrics
    current_stats = current_year_data.aggregate(
        total_revenue=Sum('revenue'),
        total_profit=Sum('profit'),
        avg_profit_margin=Avg('profit_margin')
    )
    
    previous_stats = previous_year_data.aggregate(
        total_revenue=Sum('revenue'),
        total_profit=Sum('profit'),
        avg_profit_margin=Avg('profit_margin')
    )
    
    # Calculate growth rates
    revenue_growth = 0
    profit_growth = 0
    
    if previous_stats['total_revenue'] and current_stats['total_revenue']:
        revenue_growth = ((current_stats['total_revenue'] - previous_stats['total_revenue']) / previous_stats['total_revenue']) * 100
    
    if previous_stats['total_profit'] and current_stats['total_profit']:
        profit_growth = ((current_stats['total_profit'] - previous_stats['total_profit']) / previous_stats['total_profit']) * 100
    
    # Monthly data for charts (last 12 months)
    monthly_data = []
    today = timezone.now().date()
    
    for i in range(12):
        month_start = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        month_data = DailyFinancialData.objects.filter(
            company=company,
            date__year=month_start.year,
            date__month=month_start.month
        ).aggregate(
            revenue=Sum('revenue'),
            profit=Sum('profit')
        )
        
        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(month_data['revenue'] or 0),
            'profit': float(month_data['profit'] or 0)
        })
    
    # Top performing days
    top_days = DailyFinancialData.objects.filter(
        company=company,
        year=current_year
    ).order_by('-revenue')[:5]
    
    # Latest data
    latest_data = DailyFinancialData.objects.filter(company=company).first()
    
    context = {
        'company': company,
        'latest_data': latest_data,
        'current_year_stats': current_stats,
        'previous_year_stats': previous_stats,
        'revenue_growth': round(revenue_growth, 2),
        'profit_growth': round(profit_growth, 2),
        'monthly_data': json.dumps(monthly_data[::-1]),
        'top_performing_days': top_days,
        'current_year': current_year,
    }
    
    return render(request, 'ceo_dashboard.html', context)

def hr_home(request):
    return render(request, 'hr_home.html')

def employee_home(request):
    return render(request, 'employee_home.html')

def document(request):
    return render(request, 'document.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

# API endpoint for dynamic data
@login_required
def api_financial_data(request):
    """API endpoint for chart data"""
    company = Company.objects.first()
    if not company:
        return JsonResponse({'error': 'No company data'}, status=404)
    
    period = int(request.GET.get('period', 30))
    
    data = DailyFinancialData.objects.filter(company=company).order_by('-date')[:period]
    
    chart_data = {
        'labels': [item.date.strftime('%Y-%m-%d') for item in reversed(data)],
        'revenue': [float(item.revenue) for item in reversed(data)],
        'expenditure': [float(item.expenditure) for item in reversed(data)],
        'profit': [float(item.profit) for item in reversed(data)],
        'profit_margin': [float(item.profit_margin) for item in reversed(data)],
    }
    
    return JsonResponse(chart_data)
