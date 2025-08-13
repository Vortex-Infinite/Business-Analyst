from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Avg, Max, Min, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import DailyFinancialData, Company, QuarterlySummary, YearlySummary, UserProfile

def index_view(request):
    """Enhanced landing page with real data preview"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    # Get latest company data for preview
    try:
        company = Company.objects.first()
        latest_data = DailyFinancialData.objects.filter(company=company).first()
        
        context = {
            'company': company,
            'latest_revenue': latest_data.revenue if latest_data else 0,
            'latest_profit': latest_data.profit if latest_data else 0,
            'latest_profit_margin': latest_data.profit_margin if latest_data else 0,
        }
    except:
        context = {}
    
    return render(request, 'index.html', context)

@login_required
def dashboard_view(request):
    """Main dashboard with real financial data"""
    user_profile = getattr(request.user, 'userprofile', None)
    
    if user_profile and user_profile.role == 'ceo':
        return ceo_dashboard_view(request)
    else:
        return analyst_dashboard_view(request)

@login_required
def ceo_dashboard_view(request):
    """CEO dashboard with comprehensive analytics"""
    company = Company.objects.first()
    
    # Get current date and calculate periods
    today = timezone.now().date()
    current_year = today.year
    current_quarter = f"Q{((today.month - 1) // 3) + 1}"
    
    # Latest financial metrics
    latest_data = DailyFinancialData.objects.filter(company=company).first()
    
    # Monthly performance (last 12 months)
    monthly_data = []
    for i in range(12):
        month_date = today.replace(day=1) - timedelta(days=30 * i)
        month_stats = DailyFinancialData.objects.filter(
            company=company,
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(
            total_revenue=Sum('revenue'),
            total_profit=Sum('profit'),
            avg_profit_margin=Avg('profit_margin')
        )
        
        monthly_data.append({
            'month': month_date.strftime('%b %Y'),
            'revenue': float(month_stats['total_revenue'] or 0),
            'profit': float(month_stats['total_profit'] or 0),
            'profit_margin': float(month_stats['avg_profit_margin'] or 0)
        })
    
    # Year-over-year comparison
    current_year_stats = DailyFinancialData.objects.filter(
        company=company,
        year=current_year
    ).aggregate(
        total_revenue=Sum('revenue'),
        total_profit=Sum('profit'),
        avg_profit_margin=Avg('profit_margin')
    )
    
    previous_year_stats = DailyFinancialData.objects.filter(
        company=company,
        year=current_year - 1
    ).aggregate(
        total_revenue=Sum('revenue'),
        total_profit=Sum('profit'),
        avg_profit_margin=Avg('profit_margin')
    )
    
    # Calculate growth rates
    revenue_growth = 0
    profit_growth = 0
    
    if previous_year_stats['total_revenue']:
        revenue_growth = ((current_year_stats['total_revenue'] - previous_year_stats['total_revenue']) / previous_year_stats['total_revenue']) * 100
    
    if previous_year_stats['total_profit']:
        profit_growth = ((current_year_stats['total_profit'] - previous_year_stats['total_profit']) / previous_year_stats['total_profit']) * 100
    
    # Performance insights
    top_performing_days = DailyFinancialData.objects.filter(
        company=company,
        date__year=current_year
    ).order_by('-profit_margin')[:5]
    
    # Quarterly summaries
    quarterly_summaries = QuarterlySummary.objects.filter(
        company=company
    ).order_by('-year', '-quarter')[:8]
    
    context = {
        'company': company,
        'latest_data': latest_data,
        'monthly_data': json.dumps(monthly_data[::-1]),  # Reverse for chronological order
        'current_year_stats': current_year_stats,
        'previous_year_stats': previous_year_stats,
        'revenue_growth': round(revenue_growth, 2),
        'profit_growth': round(profit_growth, 2),
        'top_performing_days': top_performing_days,
        'quarterly_summaries': quarterly_summaries,
        'current_year': current_year,
        'current_quarter': current_quarter,
    }
    
    return render(request, 'ceo_dashboard_complete.html', context)

@login_required
def analyst_dashboard_view(request):
    """Business analyst dashboard"""
    company = Company.objects.first()
    
    # Get recent data for analysis
    recent_data = DailyFinancialData.objects.filter(company=company)[:30]
    
    # Performance metrics
    performance_stats = DailyFinancialData.objects.filter(
        company=company,
        date__gte=timezone.now().date() - timedelta(days=90)
    ).aggregate(
        avg_revenue=Avg('revenue'),
        avg_profit=Avg('profit'),
        avg_profit_margin=Avg('profit_margin'),
        max_revenue=Max('revenue'),
        min_revenue=Min('revenue')
    )
    
    # Trend analysis
    trend_data = []
    for data in recent_data[:10]:
        trend_data.append({
            'date': data.date.strftime('%Y-%m-%d'),
            'revenue': float(data.revenue),
            'profit': float(data.profit),
            'profit_margin': float(data.profit_margin)
        })
    
    context = {
        'company': company,
        'recent_data': recent_data,
        'performance_stats': performance_stats,
        'trend_data': json.dumps(trend_data[::-1]),
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def api_financial_data(request):
    """API endpoint for dynamic chart data"""
    company = Company.objects.first()
    period = request.GET.get('period', '30')  # days
    
    try:
        days = int(period)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        data = DailyFinancialData.objects.filter(
            company=company,
            date__range=[start_date, end_date]
        ).order_by('date').values(
            'date', 'revenue', 'profit', 'profit_margin'
        )
        
        chart_data = {
            'labels': [item['date'].strftime('%Y-%m-%d') for item in data],
            'revenue': [float(item['revenue']) for item in data],
            'profit': [float(item['profit']) for item in data],
            'profit_margin': [float(item['profit_margin']) for item in data],
            'last_updated': timezone.now().isoformat(),
            'total_records': len(data),
        }
        
        # Add summary statistics
        if data:
            revenues = [float(item['revenue']) for item in data]
            profits = [float(item['profit']) for item in data]
            margins = [float(item['profit_margin']) for item in data]
            
            chart_data.update({
                'summary': {
                    'total_revenue': sum(revenues),
                    'avg_revenue': sum(revenues) / len(revenues),
                    'max_revenue': max(revenues),
                    'min_revenue': min(revenues),
                    'total_profit': sum(profits),
                    'avg_profit': sum(profits) / len(profits),
                    'avg_margin': sum(margins) / len(margins),
                }
            })
        
        return JsonResponse(chart_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def api_dashboard_metrics(request):
    """API endpoint for dashboard metrics refresh"""
    company = Company.objects.first()
    
    try:
        # Get latest data
        latest_data = DailyFinancialData.objects.filter(company=company).first()
        
        # Get current year stats
        current_year = timezone.now().date().year
        current_year_stats = DailyFinancialData.objects.filter(
            company=company,
            year=current_year
        ).aggregate(
            total_revenue=Sum('revenue'),
            total_profit=Sum('profit'),
            avg_profit_margin=Avg('profit_margin'),
            record_count=Count('id')
        )
        
        # Get this month's stats
        current_month = timezone.now().date().replace(day=1)
        month_stats = DailyFinancialData.objects.filter(
            company=company,
            date__gte=current_month
        ).aggregate(
            monthly_revenue=Sum('revenue'),
            monthly_profit=Sum('profit'),
            monthly_avg_margin=Avg('profit_margin')
        )
        
        # Recent performance (last 7 days)
        week_ago = timezone.now().date() - timedelta(days=7)
        recent_performance = DailyFinancialData.objects.filter(
            company=company,
            date__gte=week_ago
        ).aggregate(
            week_revenue=Sum('revenue'),
            week_profit=Sum('profit'),
            best_day_revenue=Max('revenue'),
            worst_day_revenue=Min('revenue')
        )
        
        metrics_data = {
            'latest_data': {
                'date': latest_data.date.isoformat() if latest_data else None,
                'revenue': float(latest_data.revenue) if latest_data else 0,
                'profit': float(latest_data.profit) if latest_data else 0,
                'profit_margin': float(latest_data.profit_margin) if latest_data else 0,
            },
            'current_year': {
                'total_revenue': float(current_year_stats['total_revenue'] or 0),
                'total_profit': float(current_year_stats['total_profit'] or 0),
                'avg_profit_margin': float(current_year_stats['avg_profit_margin'] or 0),
                'record_count': current_year_stats['record_count'],
            },
            'current_month': {
                'revenue': float(month_stats['monthly_revenue'] or 0),
                'profit': float(month_stats['monthly_profit'] or 0),
                'avg_margin': float(month_stats['monthly_avg_margin'] or 0),
            },
            'recent_performance': {
                'week_revenue': float(recent_performance['week_revenue'] or 0),
                'week_profit': float(recent_performance['week_profit'] or 0),
                'best_day': float(recent_performance['best_day_revenue'] or 0),
                'worst_day': float(recent_performance['worst_day_revenue'] or 0),
            },
            'last_updated': timezone.now().isoformat(),
            'company_name': company.name if company else 'N/A',
        }
        
        return JsonResponse(metrics_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def hr_login_view(request):
    """HR/CEO login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('core:dashboard')
        else:
            return render(request, 'hr_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'hr_login.html')

def employee_login_view(request):
    """Employee/Analyst login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('core:dashboard')
        else:
            return render(request, 'employee_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'employee_login.html')

def logout_view(request):
    logout(request)
    return redirect('core:index')

@login_required  
def analytics_view(request):
    """Advanced analytics page"""
    company = Company.objects.first()
    
    # Yearly performance comparison
    yearly_summaries = YearlySummary.objects.filter(company=company).order_by('year')
    
    # Seasonal analysis
    seasonal_data = DailyFinancialData.objects.filter(company=company).values('month').annotate(
        avg_revenue=Avg('revenue'),
        avg_profit=Avg('profit'),
        avg_profit_margin=Avg('profit_margin')
    ).order_by('month')
    
    context = {
        'company': company,
        'yearly_summaries': yearly_summaries,
        'seasonal_data': seasonal_data,
    }
    
    return render(request, 'dashboard.html', context)
