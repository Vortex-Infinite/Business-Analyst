from django.core.management.base import BaseCommand
from django.utils import timezone
import threading
import time
import sqlite3
import uuid
import random
from datetime import datetime
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
import os
from django.db import connection
from core.models import Transaction, Account, BalanceHistory, AnomalyAlert
from decimal import Decimal

class Command(BaseCommand):
    help = 'Run the transaction generator and anomaly detection system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--daemon',
            action='store_true',
            help='Run in daemon mode (continuous)',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of transactions to generate (default: 10)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting Transaction Generator and Anomaly Detection System...')
        )
        
        # Initialize the system
        self.init_system()
        
        if options['daemon']:
            self.run_daemon_mode()
        else:
            self.run_batch_mode(options['count'])

    def init_system(self):
        """Initialize the transaction system"""
        # Create TechCorp account if it doesn't exist
        account, created = Account.objects.get_or_create(
            account_name="TechCorp Solutions",
            defaults={
                'balance': 5000000,  # 50 lakhs
                'account_type': 'Current Account',
                'account_number': '1234567890'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created TechCorp account with balance: ₹{account.balance:,.2f}')
            )
        
        # Initialize or load the anomaly detection model
        self.model = self.load_or_train_model()
        
        self.stdout.write(
            self.style.SUCCESS('System initialized successfully')
        )

    def load_or_train_model(self):
        """Load or train the anomaly detection model"""
        model_file = "isolation_forest_model.pkl"
        
        if os.path.exists(model_file):
            try:
                model = joblib.load(model_file)
                self.stdout.write('Loaded existing anomaly detection model')
                return model
            except:
                pass
        
        # Train new model with bootstrap data
        self.stdout.write('Training new anomaly detection model...')
        historical_data = self.bootstrap_training_data()
        model = IsolationForest(contamination=0.2, random_state=42)
        model.fit(historical_data)
        joblib.dump(model, model_file)
        
        self.stdout.write('Anomaly detection model trained and saved')
        return model

    def bootstrap_training_data(self, n=80):
        """Generate synthetic normal transaction data to start the model"""
        data = [[1000], [40000]]
        data += [[round(random.triangular(1000, 20000, 40000), 2)] for _ in range(n-2)]
        return np.array(data)

    def get_balance(self):
        """Get current account balance"""
        account = Account.objects.get(account_name="TechCorp Solutions")
        return float(account.balance)

    def update_balance(self, transaction_id, amount, is_credit):
        """Update account balance and record history"""
        account = Account.objects.get(account_name="TechCorp Solutions")
        
        # Convert amount to Decimal
        amount_decimal = Decimal(str(amount))
        
        if is_credit:
            account.balance += amount_decimal
        else:
            account.balance -= amount_decimal
        
        account.save()
        
        return account.balance

    def generate_transaction(self, anomaly_rate=0.3):
        """Generate a single transaction"""
        company_names = [
            "SilverPeak Solutions", "NovaEdge Technologies", "BlueHaven Enterprises",
            "IronLeaf Systems", "Cloudspire Innovations", "BrightForge Labs",
            "Emberline Networks", "QuantumSprout Inc.", "Redwood Analytics",
            "AeroLink Dynamics", "PixelWave Studios", "Starcrest Ventures",
            "Boldstream Technologies", "ZenithPath Consulting", "LunarBay Software",
            "SwiftRock Logistics", "GreenAxis Energy", "Nexora Digital",
            "SummitCore Global", "OrionVista Systems"
        ]
        
        amount = round(random.uniform(1000, 40000), 2)
        
        if random.choice([True, False]):
            sender = "TechCorp Solutions"
            receiver = random.choice(company_names)
            if self.get_balance() < amount:
                return None
        else:
            sender = random.choice(company_names)
            receiver = "TechCorp Solutions"
        
        # Generate anomalies
        if random.random() < anomaly_rate:
            anomaly_type = random.choice(["high_amount", "same_account"])
            if anomaly_type == "high_amount":
                amount = round(random.uniform(200000, 500000), 2)
            elif anomaly_type == "same_account":
                sender = receiver
        
        return {
            "transaction_id": str(uuid.uuid4()),
            "timestamp": timezone.now(),
            "amount": amount,
            "sender": sender,
            "receiver": receiver
        }

    def save_transaction(self, transaction_data):
        """Save transaction to database"""
        if transaction_data['sender'] == transaction_data['receiver']:
            self.stdout.write(f"[SKIP] Self-transfer skipped: {transaction_data}")
            return None
        
        # Update balance if TechCorp is involved
        if transaction_data['sender'] == "TechCorp Solutions":
            new_balance = self.update_balance(
                transaction_data['transaction_id'], 
                transaction_data['amount'], 
                is_credit=False
            )
        elif transaction_data['receiver'] == "TechCorp Solutions":
            new_balance = self.update_balance(
                transaction_data['transaction_id'], 
                transaction_data['amount'], 
                is_credit=True
            )
        else:
            new_balance = self.get_balance()
        
        # Detect anomaly
        prediction = self.model.predict([[transaction_data['amount']]])
        is_anomaly = prediction[0] == -1
        anomaly_score = self.model.decision_function([[transaction_data['amount']]])[0]
        
        # Save transaction
        transaction = Transaction.objects.create(
            transaction_id=transaction_data['transaction_id'],
            timestamp=transaction_data['timestamp'],
            amount=Decimal(str(transaction_data['amount'])),
            sender=transaction_data['sender'],
            receiver=transaction_data['receiver'],
            balance=new_balance,
            is_anomaly=is_anomaly,
            anomaly_score=anomaly_score
        )
        
        # Record balance change after transaction is created
        if transaction_data['sender'] == "TechCorp Solutions" or transaction_data['receiver'] == "TechCorp Solutions":
            amount_decimal = Decimal(str(transaction_data['amount']))
            is_credit = transaction_data['receiver'] == "TechCorp Solutions"
            
            BalanceHistory.objects.create(
                transaction=transaction,
                timestamp=timezone.now(),
                change_amount=amount_decimal if is_credit else -amount_decimal,
                new_balance=new_balance
            )
        
        # Create anomaly alert if detected
        if is_anomaly:
            self.create_anomaly_alert(transaction, anomaly_score)
        
        return transaction

    def create_anomaly_alert(self, transaction, anomaly_score):
        """Create anomaly alert for suspicious transactions"""
        if transaction.amount > 100000:
            alert_type = "LARGE_AMOUNT"
            severity = "HIGH"
            title = "Large Transaction Alert"
            description = f"Transaction amount ₹{transaction.amount:,.2f} exceeds normal threshold"
        elif transaction.sender == transaction.receiver:
            alert_type = "SELF_TRANSFER"
            severity = "MEDIUM"
            title = "Self-Transfer Alert"
            description = "Transaction attempted between same account"
        else:
            alert_type = "ANOMALY_DETECTED"
            severity = "MEDIUM"
            title = "Anomaly Detected"
            description = f"Unusual transaction pattern detected (score: {anomaly_score:.3f})"
        
        AnomalyAlert.objects.create(
            transaction=transaction,
            alert_type=alert_type,
            severity=severity,
            title=title,
            description=description,
            anomaly_score=anomaly_score,
            current_value=Decimal(str(transaction.amount))
        )

    def run_batch_mode(self, count):
        """Run transaction generator for a specific number of transactions"""
        self.stdout.write(f'Generating {count} transactions...')
        
        for i in range(count):
            transaction_data = self.generate_transaction()
            if transaction_data:
                transaction = self.save_transaction(transaction_data)
                if transaction:
                    status = "ANOMALY" if transaction.is_anomaly else "NORMAL"
                    self.stdout.write(
                        f'[{status}] Transaction {i+1}: {transaction.sender} → {transaction.receiver} '
                        f'₹{transaction.amount:,.2f} | Balance: ₹{transaction.balance:,.2f}'
                    )
            
            time.sleep(1)  # Small delay between transactions
        
        self.stdout.write(
            self.style.SUCCESS(f'Generated {count} transactions successfully')
        )

    def run_daemon_mode(self):
        """Run transaction generator in continuous mode"""
        self.stdout.write('Running in daemon mode (press Ctrl+C to stop)...')
        
        try:
            while True:
                transaction_data = self.generate_transaction()
                if transaction_data:
                    transaction = self.save_transaction(transaction_data)
                    if transaction:
                        status = "ANOMALY" if transaction.is_anomaly else "NORMAL"
                        self.stdout.write(
                            f'[{status}] {transaction.sender} → {transaction.receiver} '
                            f'₹{transaction.amount:,.2f} | Balance: ₹{transaction.balance:,.2f}'
                        )
                
                time.sleep(5)  # Wait 5 seconds between transactions
                
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.SUCCESS('\nTransaction generator stopped by user')
            )
