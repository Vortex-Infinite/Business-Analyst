from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from decimal import Decimal

# class User(AbstractUser):
#     """Custom User model extending Django's AbstractUser"""
#     # Add any additional fields you need here
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     
#     def __str__(self):
#         return self.username

class Company(models.Model):
    """Company model for storing company information"""
    name = models.CharField(max_length=200)
    ticker_symbol = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='United States')
    founded_year = models.IntegerField(blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class DailyFinancialData(models.Model):
    """Daily financial data for companies"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='daily_data')
    date = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    
    # Revenue and Sales
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Expenses
    expenditure = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    operating_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cost_of_goods_sold = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Profit and Margins
    profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gross_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    
    # Assets and Liabilities
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_and_equivalents = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Key Metrics
    ebitda = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ebit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    free_cash_flow = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Market Data
    stock_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume = models.IntegerField(default=0)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    # Additional Metrics
    customer_count = models.IntegerField(default=0)
    transaction_count = models.IntegerField(default=0)
    average_transaction_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['company', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['company', 'date']),
            models.Index(fields=['date']),
            models.Index(fields=['year', 'month']),
        ]
    
    def __str__(self):
        return f"{self.company.name} - {self.date}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate year, month, day
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day
        
        # Auto-calculate profit margin if revenue > 0
        if self.revenue > 0:
            self.profit_margin = (self.profit / self.revenue) * 100
        
        super().save(*args, **kwargs)

class QuarterlySummary(models.Model):
    """Quarterly financial summaries"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='quarterly_data')
    year = models.IntegerField()
    quarter = models.IntegerField()  # 1, 2, 3, 4
    
    # Quarterly totals
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    avg_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Growth metrics
    revenue_growth = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    profit_growth = models.DecimalField(max_digits=5, decimal_places=2, default=0)   # Percentage
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['company', 'year', 'quarter']
        ordering = ['-year', '-quarter']
    
    def __str__(self):
        return f"{self.company.name} - Q{self.quarter} {self.year}"

class UserProfile(models.Model):
    """Extended user profile for business analytics"""
    from django.contrib.auth.models import User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=50, choices=[
        ('CEO', 'Chief Executive Officer'),
        ('CFO', 'Chief Financial Officer'),
        ('ANALYST', 'Business Analyst'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    ], default='EMPLOYEE')
    
    department = models.CharField(max_length=100, blank=True, null=True)
    access_level = models.CharField(max_length=20, choices=[
        ('BASIC', 'Basic Access'),
        ('STANDARD', 'Standard Access'),
        ('PREMIUM', 'Premium Access'),
        ('EXECUTIVE', 'Executive Access'),
    ], default='BASIC')
    
    preferred_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    dashboard_preferences = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class FinancialAlert(models.Model):
    """Financial alerts and notifications"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50, choices=[
        ('REVENUE_DROP', 'Revenue Drop'),
        ('PROFIT_LOSS', 'Profit Loss'),
        ('EXPENSE_SPIKE', 'Expense Spike'),
        ('MARGIN_DECLINE', 'Margin Decline'),
        ('CASH_FLOW', 'Cash Flow Issue'),
        ('PERFORMANCE', 'Performance Alert'),
    ])
    
    severity = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ], default='MEDIUM')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    threshold_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company.name} - {self.alert_type} - {self.severity}"

class DataImportLog(models.Model):
    """Log for tracking data imports"""
    from django.contrib.auth.models import User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    import_type = models.CharField(max_length=50, choices=[
        ('CSV', 'CSV Import'),
        ('EXCEL', 'Excel Import'),
        ('API', 'API Import'),
        ('MANUAL', 'Manual Entry'),
    ])
    
    file_name = models.CharField(max_length=255, blank=True, null=True)
    records_imported = models.IntegerField(default=0)
    records_failed = models.IntegerField(default=0)
    import_date = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('PARTIAL', 'Partially Completed'),
    ], default='PENDING')
    
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.import_type} - {self.import_date} - {self.status}"
