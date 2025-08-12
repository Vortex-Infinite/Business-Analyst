import csv
import os
from glob import glob
from decimal import Decimal
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Company, DailyFinancialData

class Command(BaseCommand):
    help = 'Import financial data from CSV files'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('--company-name', type=str, default='ORBIS Financial', help='Company name')
    
    def handle(self, *args, **options):
        csv_path = options['csv_file']
        company_name = options['company_name']

        # Get or create company
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={
                'symbol': 'ORBIS',
                'sector': 'Financial Services',
                'description': 'Business Intelligence and Financial Analytics Platform'
            }
        )

        if created:
            self.stdout.write(f"Created company: {company.name}")

        # Build list of files to process
        files_to_process = []
        if os.path.isdir(csv_path):
            files_to_process = sorted(glob(os.path.join(csv_path, '*.csv')))
            if not files_to_process:
                self.stdout.write(self.style.WARNING(f"No CSV files found in directory: {csv_path}"))
                return
            self.stdout.write(f"Found {len(files_to_process)} CSV files in '{csv_path}'. Starting import...")
        else:
            files_to_process = [csv_path]

        total_imported = 0
        total_skipped = 0

        for file_path in files_to_process:
            imported_count, skipped_count = self._import_single_file(file_path, company)
            total_imported += imported_count
            total_skipped += skipped_count
            self.stdout.write(self.style.SUCCESS(f"Imported {imported_count} records from '{os.path.basename(file_path)}' (skipped {skipped_count})."))

        self.stdout.write(self.style.SUCCESS(f"Import completed! Imported: {total_imported}, Skipped: {total_skipped}"))

        # Generate summary data
        self.generate_quarterly_summaries(company)
        self.generate_yearly_summaries(company)

    def _get_first(self, row, keys, default=None):
        for key in keys:
            if key in row and row[key] not in [None, '']:
                return row[key]
        return default

    def _import_single_file(self, csv_file, company):
        imported_count = 0
        skipped_count = 0
        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)

                with transaction.atomic():
                    for row in reader:
                        try:
                            # Parse date
                            date_str = self._get_first(row, ['date', 'Date'])
                            if not date_str:
                                continue

                            date_obj = datetime.strptime(str(date_str).strip(), '%Y-%m-%d').date()

                            # Check if record already exists
                            if DailyFinancialData.objects.filter(company=company, date=date_obj).exists():
                                skipped_count += 1
                                continue

                            # Convert financial data with flexible keys
                            revenue = self.safe_decimal(self._get_first(row, ['revenue', 'Revenue'], '0'))
                            sales = self.safe_decimal(self._get_first(row, ['sales', 'Sales'], '0'))
                            expenditure = self.safe_decimal(self._get_first(row, ['expenditure', 'Expenditure', 'expenses', 'Expenses'], '0'))
                            profit = self.safe_decimal(self._get_first(row, ['profit', 'Profit'], '0'))
                            profit_margin = self.safe_decimal(self._get_first(row, ['profitmargin', 'profit_margin', 'ProfitMargin', 'Profit Margin'], '0'))

                            DailyFinancialData.objects.create(
                                company=company,
                                date=date_obj,
                                day_of_week=self._get_first(row, ['dayofweek', 'day_of_week', 'DayOfWeek', 'Day of Week'], ''),
                                month=self._get_first(row, ['month', 'Month'], ''),
                                year=int(self._get_first(row, ['year', 'Year'], date_obj.year)),
                                quarter=self._get_first(row, ['quarter', 'Quarter'], 'Q1'),
                                revenue=revenue,
                                sales=sales,
                                expenditure=expenditure,
                                profit=profit,
                                profit_margin=profit_margin,
                                cumulative_revenue=self.safe_decimal(self._get_first(row, ['cumulativerevenue', 'cumulative_revenue', 'CumulativeRevenue'], '0')),
                                cumulative_profit=self.safe_decimal(self._get_first(row, ['cumulativeprofit', 'cumulative_profit', 'CumulativeProfit'], '0')),
                                revenue_growth_rate=self.safe_decimal(self._get_first(row, ['revenuegrowthrate', 'revenue_growth_rate', 'RevenueGrowthRate'])),
                                profit_growth_rate=self.safe_decimal(self._get_first(row, ['profitgrowthrate', 'profit_growth_rate', 'ProfitGrowthRate'])),
                                rolling_avg_revenue_7d=self.safe_decimal(self._get_first(row, ['rollingavgrevenue7d', 'rolling_avg_revenue_7d', 'RollingAvgRevenue7d'])),
                                rolling_avg_revenue_30d=self.safe_decimal(self._get_first(row, ['rollingavgrevenue30d', 'rolling_avg_revenue_30d', 'RollingAvgRevenue30d'])),
                            )
                            imported_count += 1

                            if imported_count % 100 == 0:
                                self.stdout.write(f"Imported {imported_count} records...")

                        except Exception as e:
                            self.stdout.write(f"Error processing row: {e}")
                            continue

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
        return imported_count, skipped_count
    
    def safe_decimal(self, value):
        """Safely convert string to Decimal"""
        if not value or value in ['', 'None', 'null']:
            return None
        try:
            return Decimal(str(value).replace(',', ''))
        except:
            return None
    
    def generate_quarterly_summaries(self, company):
        """Generate quarterly summary data"""
        from django.db.models import Sum, Avg, Max, Min, Count, Q
        from core.models import QuarterlySummary
        
        # Get all unique year-quarter combinations
        quarters = DailyFinancialData.objects.filter(company=company).values('year', 'quarter').distinct()
        
        for q in quarters:
            quarter_data = DailyFinancialData.objects.filter(
                company=company,
                year=q['year'],
                quarter=q['quarter']
            ).aggregate(
                total_revenue=Sum('revenue'),
                total_sales=Sum('sales'),
                total_expenditure=Sum('expenditure'),
                total_profit=Sum('profit'),
                avg_profit_margin=Avg('profit_margin'),
                best_day_revenue=Max('revenue'),
                worst_day_revenue=Min('revenue'),
                days_profitable=Count('id', filter=Q(profit__gt=0)),
                days_in_quarter=Count('id')
            )
            
            QuarterlySummary.objects.update_or_create(
                company=company,
                year=q['year'],
                quarter=q['quarter'],
                defaults=quarter_data
            )
        
        self.stdout.write("Generated quarterly summaries")
    
    def generate_yearly_summaries(self, company):
        """Generate yearly summary data"""
        from django.db.models import Sum, Avg
        from core.models import YearlySummary
        
        years = DailyFinancialData.objects.filter(company=company).values('year').distinct()
        
        for y in years:
            year_data = DailyFinancialData.objects.filter(
                company=company,
                year=y['year']
            ).aggregate(
                total_revenue=Sum('revenue'),
                total_profit=Sum('profit'),
                avg_daily_revenue=Avg('revenue'),
                avg_profit_margin=Avg('profit_margin')
            )
            
            YearlySummary.objects.update_or_create(
                company=company,
                year=y['year'],
                defaults=year_data
            )
        
        self.stdout.write("Generated yearly summaries")
