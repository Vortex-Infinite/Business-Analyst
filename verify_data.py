import os
import django
import sys
from datetime import date

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import DailyTransactionSummary, Transaction

def verify():
    print("Verifying data...")
    today = date.today()
    
    # Check transactions
    tx_count = Transaction.objects.filter(timestamp__date=today).count()
    print(f"Transactions today: {tx_count}")
    
    # Check summary
    summary = DailyTransactionSummary.objects.filter(date=today).first()
    if summary:
        print(f"Summary found for {summary.date}:")
        print(f"  Total Transactions: {summary.total_transactions}")
        print(f"  Total Amount: {summary.total_amount}")
        print(f"  Anomalies: {summary.anomaly_count}")
        print(f"  Avg Value: {summary.avg_transaction_value}")
        
        if summary.total_transactions == tx_count:
             print("SUCCESS: Summary count matches transaction count.")
        else:
             print(f"WARNING: Summary count ({summary.total_transactions}) does not match transaction count ({tx_count}). (Might be due to concurrency)")
    else:
        print("FAIL: No summary found for today.")

if __name__ == "__main__":
    verify()
