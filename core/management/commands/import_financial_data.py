import csv
import os
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from core.models import Company, DailyFinancialData, QuarterlySummary, DataImportLog
import re

class Command(BaseCommand):
    help = 'Import financial data from CSV files in the Dataset folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Specific CSV file to import (daily, monthly, quarterly, yearly)',
        )
        parser.add_argument(
            '--company-name',
            type=str,
            default='Sample Company',
            help='Company name for the imported data',
        )

    def clean_currency_value(self, value):
        """Clean currency values from CSV format"""
        if not value or value.strip() == '':
            return Decimal('0.00')
        
        # Remove currency symbols, commas, and extra spaces
        cleaned = re.sub(r'[₹\s,?]', '', str(value).strip())
        
        # Handle negative values
        if cleaned.startswith('-'):
            cleaned = '-' + cleaned[1:].replace('-', '')
        
        try:
            return Decimal(cleaned)
        except:
            return Decimal('0.00')

    def parse_date(self, date_str):
        """Parse date string in DD-MM-YYYY format"""
        try:
            return datetime.strptime(date_str.strip(), '%d-%m-%Y').date()
        except:
            return None

    def handle(self, *args, **options):
        company_name = options['company_name']
        file_type = options.get('file')
        
        # Create or get company
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={
                'industry': 'Technology',
                'sector': 'Software',
                'country': 'India',
                'description': f'Company created from imported financial data'
            }
        )
        
        if created:
            self.stdout.write(f"Created new company: {company.name}")
        else:
            self.stdout.write(f"Using existing company: {company.name}")

        # Create import log
        import_log = DataImportLog.objects.create(
            user=User.objects.first() if User.objects.exists() else None,
            import_type='CSV',
            status='IN_PROGRESS'
        )

        try:
            dataset_path = os.path.join(os.getcwd(), 'Dataset')
            
            if file_type:
                files_to_process = [f'financial_data_{file_type}_cashflow.csv']
            else:
                files_to_process = [
                    'financial_data_daily_cashflow.csv',
                    'financial_data_monthly_cashflow.csv',
                    'financial_data_quarterly_cashflow.csv',
                    'financial_data_yearly_cashflow.csv'
                ]

            total_imported = 0
            total_failed = 0

            for filename in files_to_process:
                file_path = os.path.join(dataset_path, filename)
                
                if not os.path.exists(file_path):
                    self.stdout.write(f"File not found: {file_path}")
                    continue

                self.stdout.write(f"Processing {filename}...")
                
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    
                    records_imported = 0
                    records_failed = 0
                    
                    for row in reader:
                        try:
                            if 'Date' in row and row['Date']:
                                # Parse date
                                date = self.parse_date(row['Date'])
                                if not date:
                                    records_failed += 1
                                    continue
                                
                                # Clean and parse values
                                revenue = self.clean_currency_value(row.get('Revenue', 0))
                                expenses = self.clean_currency_value(row.get('Expenses', 0))
                                income = self.clean_currency_value(row.get('Income', 0))
                                cash_flow = self.clean_currency_value(row.get('Cash_Flow', 0))
                                
                                # Create daily financial data
                                daily_data, created = DailyFinancialData.objects.get_or_create(
                                    company=company,
                                    date=date,
                                    defaults={
                                        'revenue': revenue,
                                        'expenditure': expenses,
                                        'profit': income,
                                        'free_cash_flow': cash_flow,
                                        'year': date.year,
                                        'month': date.month,
                                        'day': date.day,
                                    }
                                )
                                
                                if not created:
                                    # Update existing record
                                    daily_data.revenue = revenue
                                    daily_data.expenditure = expenses
                                    daily_data.profit = income
                                    daily_data.free_cash_flow = cash_flow
                                    daily_data.save()
                                
                                records_imported += 1
                                
                                # Create quarterly summary if quarter info is available
                                if 'Quarter' in row and row['Quarter']:
                                    try:
                                        quarter = int(float(row['Quarter']))
                                        year = date.year
                                        
                                        quarterly_summary, created = QuarterlySummary.objects.get_or_create(
                                            company=company,
                                            year=year,
                                            quarter=quarter,
                                            defaults={
                                                'total_revenue': revenue,
                                                'total_expenses': expenses,
                                                'total_profit': income,
                                            }
                                        )
                                        
                                        if not created:
                                            # Update quarterly totals
                                            quarterly_summary.total_revenue += revenue
                                            quarterly_summary.total_expenses += expenses
                                            quarterly_summary.total_profit += income
                                            quarterly_summary.save()
                                            
                                    except (ValueError, TypeError):
                                        pass
                                        
                        except Exception as e:
                            records_failed += 1
                            self.stdout.write(f"Error processing row: {e}")
                    
                    total_imported += records_imported
                    total_failed += records_failed
                    
                    self.stdout.write(f"  Imported: {records_imported}, Failed: {records_failed}")

            # Update import log
            import_log.records_imported = total_imported
            import_log.records_failed = total_failed
            import_log.status = 'COMPLETED'
            import_log.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully imported financial data!\n'
                    f'Total records imported: {total_imported}\n'
                    f'Total records failed: {total_failed}\n'
                    f'Company: {company.name}'
                )
            )

        except Exception as e:
            import_log.status = 'FAILED'
            import_log.error_message = str(e)
            import_log.save()
            
            self.stdout.write(
                self.style.ERROR(f'Import failed: {e}')
            )
