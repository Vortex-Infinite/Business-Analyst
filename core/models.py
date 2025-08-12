from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     """Custom User model extending Django's AbstractUser"""
#     # Add any additional fields you need here
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
    
#     def __str__(self):
#         return self.username

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import uuid

class Company(models.Model):
    """Company information"""
    name = models.CharField(max_length=200, default="ORBIS Financial")
    symbol = models.CharField(max_length=10, default="ORBIS")
    sector = models.CharField(max_length=100, default="Financial Services")
    description = models.TextField(blank=True)
    founded_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class DailyFinancialData(models.Model):
    """Main financial data model matching your CSV structure"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='daily_data')
    
    # Basic date information
    date = models.DateField(db_index=True)
    day_of_week = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    year = models.IntegerField(db_index=True)
    quarter = models.CharField(max_length=2, db_index=True)
    
    # Core financial metrics
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    sales = models.DecimalField(max_digits=15, decimal_places=2)
    expenditure = models.DecimalField(max_digits=15, decimal_places=2)
    profit = models.DecimalField(max_digits=15, decimal_places=2)
    profit_margin = models.DecimalField(max_digits=8, decimal_places=4)
    
    # Cumulative metrics
    cumulative_revenue = models.DecimalField(max_digits=20, decimal_places=2)
    cumulative_profit = models.DecimalField(max_digits=20, decimal_places=2)
    
    # Growth metrics
    revenue_growth_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    profit_growth_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Rolling averages
    rolling_avg_revenue_7d = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    rolling_avg_revenue_30d = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['company', 'date']
        indexes = [
            models.Index(fields=['date', 'company']),
            models.Index(fields=['year', 'quarter']),
            models.Index(fields=['profit_margin']),
        ]
    
    def __str__(self):
        return f"{self.company.name} - {self.date}"
    
    @property
    def performance_status(self):
        """Determine performance status based on profit margin"""
        if self.profit_margin >= 30:
            return 'excellent'
        elif self.profit_margin >= 20:
            return 'good'
        elif self.profit_margin >= 10:
            return 'average'
        elif self.profit_margin >= 0:
            return 'poor'
        else:
            return 'loss'

class QuarterlySummary(models.Model):
    """Quarterly aggregated data"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='quarterly_summaries')
    year = models.IntegerField()
    quarter = models.CharField(max_length=2)
    
    total_revenue = models.DecimalField(max_digits=20, decimal_places=2)
    total_sales = models.DecimalField(max_digits=20, decimal_places=2)
    total_expenditure = models.DecimalField(max_digits=20, decimal_places=2)
    total_profit = models.DecimalField(max_digits=20, decimal_places=2)
    avg_profit_margin = models.DecimalField(max_digits=8, decimal_places=4)
    
    # Performance metrics
    best_day_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    worst_day_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    days_profitable = models.IntegerField()
    days_in_quarter = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['company', 'year', 'quarter']
        ordering = ['-year', '-quarter']
    
    def __str__(self):
        return f"{self.company.name} - {self.year} Q{self.quarter}"

class YearlySummary(models.Model):
    """Yearly aggregated data"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='yearly_summaries')
    year = models.IntegerField()
    
    total_revenue = models.DecimalField(max_digits=20, decimal_places=2)
    total_profit = models.DecimalField(max_digits=20, decimal_places=2)
    avg_daily_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    avg_profit_margin = models.DecimalField(max_digits=8, decimal_places=4)
    
    growth_rate_revenue = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    growth_rate_profit = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    
    class Meta:
        ordering = ['-year']
        unique_together = ['company', 'year']

class PredictionData(models.Model):
    """AI/ML predictions for future performance"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='predictions')
    prediction_date = models.DateField()
    target_date = models.DateField()
    
    predicted_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    predicted_profit = models.DecimalField(max_digits=15, decimal_places=2)
    predicted_profit_margin = models.DecimalField(max_digits=8, decimal_places=4)
    
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4)
    model_used = models.CharField(max_length=50, default='LSTM')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ('ceo', 'CEO'),
        ('analyst', 'Business Analyst'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ])
    department = models.CharField(max_length=100, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    dashboard_preferences = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"
