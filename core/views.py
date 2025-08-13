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
    # Don't automatically redirect authenticated users - let them choose
    
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
            'user_authenticated': request.user.is_authenticated,
        }
    except Exception as e:
        context = {'error': str(e), 'user_authenticated': request.user.is_authenticated}
    
    return render(request, 'index.html', context)

def hr_login(request):
    """HR/Manager login with authentication and OTP verification"""
    if request.method == 'POST':
        username = request.POST.get('hrId')  # Manager email
        password = request.POST.get('hrPassword')  # Manager password
        otp = request.POST.get('hrOtp')  # OTP code
        
        # Check OTP first (demo OTP is 123456)
        if otp != '123456':
            return render(request, 'hr_login.html', {'error': 'Invalid OTP code. Use 123456 for demo.'})
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Set session timeout to 30 minutes for security
            request.session.set_expiry(1800)
            return redirect('ceo_dashboard')  # Manager goes to CEO dashboard
        else:
            return render(request, 'hr_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'hr_login.html')

def employee_login(request):
    """Employee/Analyst login with authentication and OTP verification"""
    if request.method == 'POST':
        username = request.POST.get('employeeId')  # Analyst email
        password = request.POST.get('employeePassword')  # Analyst password
        otp = request.POST.get('employeeOtp')  # OTP code
        
        # Check OTP first (demo OTP is 123456)
        if otp != '123456':
            return render(request, 'employee_login.html', {'error': 'Invalid OTP code. Use 123456 for demo.'})
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Set session timeout to 30 minutes for security
            request.session.set_expiry(1800)
            return redirect('dashboard')  # Analyst goes to business analyst dashboard
        else:
            return render(request, 'employee_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'employee_login.html')

@login_required
def dashboard(request):
    """Updated business analyst dashboard with daily data focus"""
    company = Company.objects.first()
    
    if not company:
        return render(request, 'dashboard.html', {'error': 'No company data found. Please import financial data first.'})
    
    # Get current date (or most recent available date)
    current_date = timezone.now().date()
    
    # Get the most recent available date from the database
    latest_data = DailyFinancialData.objects.filter(company=company).order_by('-date').first()
    if latest_data:
        current_date = latest_data.date
    
    # Get daily data for the current/recent date
    daily_data_for_display = DailyFinancialData.objects.filter(
        company=company,
        date=current_date
    ).first()
    
    # Get previous day data for comparison
    previous_date = current_date - timedelta(days=1)
    previous_day_data = DailyFinancialData.objects.filter(
        company=company,
        date=previous_date
    ).first()
    
    # Get all historical data for total stats
    all_data = DailyFinancialData.objects.filter(company=company).order_by('date')
    
    if not all_data.exists():
        return render(request, 'dashboard.html', {'error': 'No financial data found. Please import financial data first.'})
    
    # Calculate daily stats (for the specific day)
    if daily_data_for_display:
        daily_stats = {
            'revenue': daily_data_for_display.revenue,
            'expenditure': daily_data_for_display.expenditure,
            'profit': daily_data_for_display.profit,
            'profit_margin': daily_data_for_display.profit_margin,
            'free_cash_flow': daily_data_for_display.free_cash_flow
        }
    else:
        daily_stats = {
            'revenue': 0,
            'expenditure': 0,
            'profit': 0,
            'profit_margin': 0,
            'free_cash_flow': 0
        }
    
    # Calculate previous day stats
    if previous_day_data:
        previous_stats = {
            'revenue': previous_day_data.revenue,
            'expenditure': previous_day_data.expenditure,
            'profit': previous_day_data.profit,
            'profit_margin': previous_day_data.profit_margin
        }
    else:
        previous_stats = {
            'revenue': 0,
            'expenditure': 0,
            'profit': 0,
            'profit_margin': 0
        }
    
    # Calculate total historical stats
    total_stats = all_data.aggregate(
        total_revenue=Sum('revenue'),
        total_expenditure=Sum('expenditure'),
        total_profit=Sum('profit'),
        avg_profit_margin=Avg('profit_margin'),
        max_revenue=Max('revenue'),
        min_revenue=Min('revenue')
    )
    
    # Calculate trends (current day vs previous day)
    revenue_trend = 0
    expense_trend = 0
    profit_trend = 0
    margin_trend = 0
    
    if previous_stats['revenue'] and daily_stats['revenue']:
        revenue_trend = ((daily_stats['revenue'] - previous_stats['revenue']) / previous_stats['revenue']) * 100
    
    if previous_stats['expenditure'] and daily_stats['expenditure']:
        expense_trend = ((daily_stats['expenditure'] - previous_stats['expenditure']) / previous_stats['expenditure']) * 100
    
    if previous_stats['profit'] and daily_stats['profit']:
        profit_trend = ((daily_stats['profit'] - previous_stats['profit']) / previous_stats['profit']) * 100
    
    if previous_stats['profit_margin'] and daily_stats['profit_margin']:
        margin_trend = daily_stats['profit_margin'] - previous_stats['profit_margin']
    
    # Enhanced performance stats with daily focus
    performance_stats = {
        'total_revenue': total_stats['total_revenue'] or 0,
        'total_expenditure': total_stats['total_expenditure'] or 0,
        'total_profit': total_stats['total_profit'] or 0,
        'actual_profit': daily_stats['profit'] or 0,
        'avg_profit_margin': total_stats['avg_profit_margin'] or 0,
        'max_revenue': total_stats['max_revenue'] or 0,
        'min_revenue': total_stats['min_revenue'] or 0,
        'revenue_trend': round(revenue_trend, 1) if revenue_trend else 0,
        'expense_trend': round(expense_trend, 1) if expense_trend else 0,
        'profit_trend': round(profit_trend, 1) if profit_trend else 0,
        'margin_trend': round(margin_trend, 1) if margin_trend else 0,
        'daily_revenue': daily_stats['revenue'] or 0,
        'daily_expenses': daily_stats['expenditure'] or 0,
        'daily_profit': daily_stats['profit'] or 0,
        'roi': round((daily_stats['profit'] / daily_stats['expenditure'] * 100), 1) if daily_stats['expenditure'] else 0
    }
    
    # Get recent daily data for charts (last 20 days)
    recent_daily_data = DailyFinancialData.objects.filter(
        company=company
    ).order_by('-date')[:20]
    
    # Prepare daily data for charts (JSON serializable)
    daily_data_for_charts = []
    for data in reversed(recent_daily_data):  # Reverse to get chronological order
        daily_data_for_charts.append({
            'date': data.date.strftime('%Y-%m-%d'),  # Convert to string for JSON
            'revenue': float(data.revenue),
            'expenditure': float(data.expenditure),
            'profit': float(data.profit),
            'profit_margin': float(data.profit_margin)
        })
    
    # Prepare daily data for template (with date objects for template formatting)
    daily_data_for_template = []
    for data in recent_daily_data:
        daily_data_for_template.append({
            'date': data.date,  # Keep as date object for template
            'revenue': float(data.revenue),
            'expenditure': float(data.expenditure),
            'profit': float(data.profit),
            'profit_margin': float(data.profit_margin)
        })
    
    # Get date range for display
    first_date = all_data.first().date
    last_date = all_data.last().date
    
    # Prepare context with daily focus
    context = {
        'company': company,
        'recent_data': recent_daily_data,
        'performance_stats': performance_stats,
        'trend_data': json.dumps(daily_data_for_charts),  # JSON serializable data
        
        # Daily data (main focus)
        'total_revenue': daily_stats['revenue'] or 0,
        'total_expenses': daily_stats['expenditure'] or 0,
        'total_profit': daily_stats['profit'] or 0,
        'recent_revenue': daily_stats['revenue'] or 0,
        'recent_expenses': daily_stats['expenditure'] or 0,
        'recent_profit': daily_stats['profit'] or 0,
        'avg_daily_revenue': daily_stats['revenue'] or 0,  # This is now the daily revenue
        'avg_daily_expenses': daily_stats['expenditure'] or 0,  # This is now the daily expenses
        'avg_daily_profit': daily_stats['profit'] or 0,  # This is now the daily profit
        'daily_data': daily_data_for_template,
        'data_period': f"Daily Data ({current_date.strftime('%B %d, %Y')})",
        'current_month': current_date.strftime('%B %d, %Y'),
        'historical_period': f"{first_date.strftime('%B %Y')} - {last_date.strftime('%B %Y')}",
        'display_date': current_date
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

def logout_all(request):
    """Clear all sessions and cookies to break redirect loops"""
    logout(request)
    # Clear all session data
    request.session.flush()
    # Clear any remaining cookies
    response = redirect('index')
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    return response

def clear_session(request):
    """Clear all browser data and start fresh"""
    logout(request)
    request.session.flush()
    
    response = render(request, 'session_cleared.html')
    # Delete all cookies
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    
    return response

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

@login_required
def analytics(request):
    """Comprehensive analytics page with dropdown options for viewing past 5 years data"""
    company = Company.objects.first()
    
    if not company:
        return render(request, 'analytics.html', {'error': 'No company data found. Please import financial data first.'})
    
    # Get the selected period from request
    period = request.GET.get('period', 'monthly')  # monthly, quarterly, yearly
    year = request.GET.get('year', '2020')  # Default to 2020 since that's our data
    
    # Get all available years from the data
    all_years = DailyFinancialData.objects.filter(company=company).values_list('date__year', flat=True).distinct().order_by('-date__year')
    
    # Get data based on selected period and year
    if period == 'monthly':
        # Monthly data for selected year
        monthly_data = []
        for month in range(1, 13):
            month_data = DailyFinancialData.objects.filter(
                company=company,
                date__year=year,
                date__month=month
            ).aggregate(
                revenue=Sum('revenue'),
                expenses=Sum('expenditure'),
                profit=Sum('profit'),
                profit_margin=Avg('profit_margin'),
                days_count=Count('id')
            )
            
            if month_data['days_count'] > 0:
                monthly_data.append({
                    'month': f"{month:02d}",
                    'month_name': f"{month:02d}",
                    'period': f"{month:02d}",  # Add period key for consistency
                    'revenue': float(month_data['revenue'] or 0),
                    'expenses': float(month_data['expenses'] or 0),
                    'profit': float(month_data['profit'] or 0),
                    'profit_margin': round(float(month_data['profit_margin'] or 0), 2),
                    'roi': round((float(month_data['profit'] or 0) / float(month_data['expenses'] or 1) * 100), 2) if month_data['expenses'] else 0
                })
        
        period_data = monthly_data
        period_label = "Monthly"
        
    elif period == 'quarterly':
        # Quarterly data for selected year
        quarterly_data = []
        for quarter in range(1, 5):
            start_month = (quarter - 1) * 3 + 1
            end_month = quarter * 3
            
            quarter_data = DailyFinancialData.objects.filter(
                company=company,
                date__year=year,
                date__month__gte=start_month,
                date__month__lte=end_month
            ).aggregate(
                revenue=Sum('revenue'),
                expenses=Sum('expenditure'),
                profit=Sum('profit'),
                profit_margin=Avg('profit_margin'),
                days_count=Count('id')
            )
            
            if quarter_data['days_count'] > 0:
                quarterly_data.append({
                    'quarter': f"Q{quarter}",
                    'period': f"Q{quarter}",
                    'revenue': float(quarter_data['revenue'] or 0),
                    'expenses': float(quarter_data['expenses'] or 0),
                    'profit': float(quarter_data['profit'] or 0),
                    'profit_margin': round(float(quarter_data['profit_margin'] or 0), 2),
                    'roi': round((float(quarter_data['profit'] or 0) / float(quarter_data['expenses'] or 1) * 100), 2) if quarter_data['expenses'] else 0
                })
        
        period_data = quarterly_data
        period_label = "Quarterly"
        
    else:  # yearly
        # Yearly data for past 5 years
        yearly_data = []
        for y in all_years[:5]:  # Last 5 years
            year_data = DailyFinancialData.objects.filter(
                company=company,
                date__year=y
            ).aggregate(
                revenue=Sum('revenue'),
                expenses=Sum('expenditure'),
                profit=Sum('profit'),
                profit_margin=Avg('profit_margin'),
                days_count=Count('id')
            )
            
            if year_data['days_count'] > 0:
                yearly_data.append({
                    'year': str(y),
                    'period': str(y),
                    'revenue': float(year_data['revenue'] or 0),
                    'expenses': float(year_data['expenses'] or 0),
                    'profit': float(year_data['profit'] or 0),
                    'profit_margin': round(float(year_data['profit_margin'] or 0), 2),
                    'roi': round((float(year_data['profit'] or 0) / float(year_data['expenses'] or 1) * 100), 2) if year_data['expenses'] else 0
                })
        
        period_data = yearly_data
        period_label = "Yearly"
    
    # Calculate summary statistics
    total_revenue = sum(item['revenue'] for item in period_data)
    total_expenses = sum(item['expenses'] for item in period_data)
    total_profit = sum(item['profit'] for item in period_data)
    avg_profit_margin = sum(item['profit_margin'] for item in period_data) / len(period_data) if period_data else 0
    avg_roi = sum(item['roi'] for item in period_data) / len(period_data) if period_data else 0
    
    # Prepare chart data
    chart_data = {
        'labels': [item['period'] for item in period_data],
        'revenue': [item['revenue'] for item in period_data],
        'expenses': [item['expenses'] for item in period_data],
        'profit': [item['profit'] for item in period_data],
        'profit_margin': [item['profit_margin'] for item in period_data],
        'roi': [item['roi'] for item in period_data]
    }
    
    context = {
        'company': company,
        'period': period,
        'year': year,
        'period_label': period_label,
        'period_data': period_data,
        'all_years': all_years,
        'chart_data': json.dumps(chart_data),
        'summary': {
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'total_profit': total_profit,
            'avg_profit_margin': round(avg_profit_margin, 2),
            'avg_roi': round(avg_roi, 2)
        }
    }
    
    return render(request, 'analytics.html', context)
