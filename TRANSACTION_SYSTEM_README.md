# ORBIS Transaction System Integration

## Overview
The ORBIS Business Analytics system now includes a comprehensive transaction management and anomaly detection system that integrates with the Django web application.

## Features

### 🔄 Live Transaction Generation
- **Automatic Transaction Generation**: Creates realistic financial transactions every 5 seconds
- **Multiple Company Simulation**: Simulates transactions between TechCorp Solutions and 20 other companies
- **Real-time Balance Updates**: Automatically updates account balances for all transactions
- **Anomaly Injection**: Intentionally generates suspicious transactions for testing

### 🛡️ Anomaly Detection
- **Machine Learning Model**: Uses Isolation Forest algorithm for anomaly detection
- **Real-time Analysis**: Analyzes each transaction as it occurs
- **Multiple Alert Types**:
  - Large Amount Alerts (transactions > ₹100,000)
  - Self-Transfer Alerts (same sender/receiver)
  - Pattern Anomalies (unusual transaction patterns)
- **Severity Levels**: Low, Medium, High, and Critical alerts

### 📊 Web Dashboard
- **Live Transaction Feed**: Real-time display of all transactions
- **Anomaly Dashboard**: Shows active alerts and their severity
- **Account Balance**: Real-time balance updates
- **Statistics**: Transaction counts, anomaly rates, and alert summaries
- **Auto-refresh**: Updates every 5 seconds automatically

## Database Models

### Transaction Model
```python
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, primary_key=True)
    timestamp = models.DateTimeField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_anomaly = models.BooleanField(default=False)
    anomaly_score = models.FloatField(null=True, blank=True)
```

### Account Model
```python
class Account(models.Model):
    account_name = models.CharField(max_length=200, primary_key=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    account_type = models.CharField(max_length=50, default='Current Account')
    account_number = models.CharField(max_length=50, blank=True, null=True)
```

### AnomalyAlert Model
```python
class AnomalyAlert(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    anomaly_score = models.FloatField()
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start the System

#### Option A: Using the Batch File (Windows)
```bash
start_orbis.bat
```

#### Option B: Manual Start
```bash
# Activate virtual environment
venv\Scripts\activate

# Start Django server
python manage.py runserver

# In another terminal, start transaction generator
python manage.py run_transaction_generator --daemon
```

#### Option C: Using the Startup Script
```bash
python start_transaction_system.py
```

## Usage

### Transaction Generator Commands

#### Generate Specific Number of Transactions
```bash
python manage.py run_transaction_generator --count 10
```

#### Run in Continuous Mode (Daemon)
```bash
python manage.py run_transaction_generator --daemon
```

### Web Interface

1. **Access the Application**: Open `http://127.0.0.1:8000/`
2. **Login**: Use the employee login with OTP `123456`
3. **Navigate to Transactions**: Click on "Transaction" in the sidebar
4. **View Live Data**: The page will automatically update every 5 seconds

### API Endpoints

#### Get Transaction Data
```
GET /api/transactions/
```
Returns:
```json
{
    "transactions": [...],
    "alerts": [...],
    "account_balance": 5000000.00,
    "total_transactions": 25,
    "anomaly_count": 3
}
```

## Configuration

### Transaction Parameters
- **Starting Balance**: ₹50,00,000 (50 lakhs)
- **Transaction Range**: ₹1,000 - ₹40,000 (normal), ₹2,00,000 - ₹5,00,000 (anomalies)
- **Generation Interval**: 5 seconds (daemon mode)
- **Anomaly Rate**: 30% (configurable)

### Anomaly Detection Settings
- **Model**: Isolation Forest
- **Contamination**: 0.2 (20% expected anomalies)
- **Training Data**: 80 synthetic transactions
- **Threshold**: Automatic based on model training

## File Structure

```
Business-Analyst/
├── core/
│   ├── models.py                 # Database models
│   ├── views.py                  # Web views and API endpoints
│   ├── urls.py                   # URL routing
│   ├── management/
│   │   └── commands/
│   │       └── run_transaction_generator.py  # Transaction generator
│   └── templates/
│       └── transaction.html      # Transaction dashboard
├── core/static/assets/js/
│   └── transaction.js            # Real-time updates
├── start_transaction_system.py   # Startup script
├── start_orbis.bat              # Windows batch file
└── requirements.txt             # Dependencies
```

## Monitoring & Logs

### Transaction Logs
- All transactions are logged to the database
- Console output shows real-time transaction status
- Anomaly detection results are displayed immediately

### Alert Management
- Active alerts are displayed in the web interface
- Alerts can be resolved or ignored
- Alert history is maintained in the database

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure migrations are applied: `python manage.py migrate`
   - Check database file permissions

2. **Transaction Generator Not Starting**
   - Verify virtual environment is activated
   - Check for missing dependencies: `pip install -r requirements.txt`

3. **Web Interface Not Updating**
   - Check browser console for JavaScript errors
   - Verify API endpoint is accessible: `/api/transactions/`

4. **Anomaly Detection Not Working**
   - Check if model file exists: `isolation_forest_model.pkl`
   - Re-run transaction generator to retrain model

### Performance Optimization
- **Database Indexing**: Models include optimized indexes
- **Caching**: Consider adding Redis for high-frequency updates
- **Background Tasks**: Use Celery for production deployment

## Security Considerations

- **Input Validation**: All transaction data is validated
- **SQL Injection Protection**: Django ORM provides protection
- **CSRF Protection**: Enabled by default
- **Session Management**: 30-minute timeout for security

## Future Enhancements

- **Real-time Notifications**: Email/SMS alerts for critical anomalies
- **Advanced Analytics**: Transaction pattern analysis
- **Multi-account Support**: Multiple company accounts
- **API Rate Limiting**: Prevent abuse of API endpoints
- **Audit Trail**: Complete transaction history and changes

