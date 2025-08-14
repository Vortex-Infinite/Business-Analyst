# 🏢 ORBIS Financial - Business Analyst Platform

A comprehensive Django-based financial analytics platform for business intelligence, CEO dashboards, and financial data management.

## 🚀 Features

- **Executive Dashboard**: Comprehensive CEO dashboard with real-time financial metrics
- **Business Analytics**: Interactive charts and financial data visualization
- **Role-based Access**: Separate portals for CEO and Financial Analysts
- **Real-time Data**: Live financial data with API endpoints
- **Responsive Design**: Modern UI with dark/light theme support
- **Financial Data Management**: Import and analyze CSV financial datasets

## 🏗️ Project Structure

```
Business-Analyst/
│
├── 📄 manage.py                    # Django's command-line utility
├── � db.sqlite3                  # SQLite database
├── 📄 LICENSE                     # Project license
├── 📄 README.md                   # This file
│
├── 📁 backend/                     # Django project configuration
│   ├── 📄 __init__.py
│   ├── 📄 asgi.py                 # ASGI configuration
│   ├── 📄 settings.py             # Django settings (database, static files, etc.)
│   ├── 📄 urls.py                 # Main URL routing
│   └── 📄 wsgi.py                 # WSGI configuration
│
├── 📁 core/                       # Main Django application
│   ├── 📄 __init__.py
│   ├── 📄 admin.py                # Django admin configuration
│   ├── 📄 apps.py                 # App configuration
│   ├── 📄 models.py               # Database models (Company, DailyFinancialData, etc.)
│   ├── 📄 views.py                # View logic and API endpoints
│   ├── 📄 urls.py                 # App-specific URL routing
│   ├── 📄 tests.py                # Unit tests
│   │
│   ├── 📁 migrations/             # Database migrations
│   │   ├── 📄 __init__.py
│   │   ├── 📄 0001_initial.py
│   │   └── ...
│   │
│   ├── 📁 static/                 # Static files (CSS, JS, Images)
│   │   └── 📁 assets/
│   │       ├── 📁 css/
│   │       │   ├── 📄 style.css           # Main stylesheet
│   │       │   ├── 📄 dashboard_style.css # Dashboard-specific styles
│   │       │   └── � ceo_dashboard_style.css # CEO dashboard styles
│   │       ├── 📁 js/
│   │       │   ├── 📄 script.js           # Main JavaScript
│   │       │   ├── 📄 dashboard.js        # Dashboard functionality
│   │       │   ├── 📄 auth.js             # Authentication logic
│   │       │   └── 📄 ceo_dashboard.js    # CEO dashboard scripts
│   │       └── 📁 images/
│   │           └── 📄 home-icon-silhouette.png
│   │
│   └── 📁 templates/              # HTML templates
│       ├── 📄 index.html          # Landing page
│       ├── 📄 hr_login.html       # Financial Analyst login
│       ├── 📄 employee_login.html # CEO login
│       ├── 📄 dashboard.html      # Main dashboard
│       ├── 📄 ceo_dashboard.html  # CEO dashboard
│       ├── 📄 hr_home.html        # HR home page
│       ├── 📄 employee_home.html  # Employee home page
│       └── 📄 document.html       # Document viewer
│
├── 📁 Dataset/                    # Financial datasets
│   ├── 📄 actual_income_dataset.csv
│   ├── 📄 expenses_2020_2025.csv
│   ├── 📄 income_2020_2025.csv
│   └── 📄 revenue_2020_2025.csv
│
├── 📁 staticfiles/               # Collected static files (production)
│   ├── 📁 admin/                # Django admin static files
│   └── 📁 assets/               # App static files
│
└── 📁 venv/                     # Python virtual environment
    └── ...
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+ 
- pip
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Vortex-Infinite/Business-Analyst.git
cd Business-Analyst
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django
pip install python-decouple  # If using environment variables
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

## 🎯 Usage

### Test Credentials

**CEO Portal:**
- Username: `ceo`
- Password: `ceo123`

**Financial Analyst Portal:**
- Username: `analyst` 
- Password: `analyst123`

**Admin Access:**
- Username: `admin`
- Password: `admin123`

### Importing Financial Data

```bash
# Import specific CSV file
python manage.py import_financial_data "Dataset/revenue_2020_2025.csv" --company-name "ORBIS Financial"

# Import all files in a directory
python manage.py import_financial_data "Dataset/" --company-name "ORBIS Financial"
```

## 🗄️ Database Models

### Key Models:
- **Company**: Company information and metadata
- **DailyFinancialData**: Daily financial metrics (revenue, profit, margins)
- **QuarterlySummary**: Quarterly aggregated data
- **YearlySummary**: Yearly financial summaries
- **UserProfile**: Extended user information with roles
- **PredictionData**: AI/ML prediction storage

## 🌐 API Endpoints

- `/api/financial-data/` - Get financial chart data
- `/api/dashboard-metrics/` - Get dashboard KPI metrics
- `/admin/` - Django admin interface

## 🎨 Frontend Technologies

- **HTML5 & CSS3**: Responsive layouts
- **JavaScript (ES6+)**: Interactive functionality
- **Chart.js**: Data visualization
- **Font Awesome**: Icons
- **Google Fonts**: Typography (Poppins)

## 🏢 Key Features Implemented

### ✅ Authentication System
- Role-based login (CEO, Analyst, Admin)
- Session management
- Secure authentication

### ✅ Financial Dashboard
- Real-time financial metrics
- Interactive charts and graphs
- Year-over-year comparisons
- Quarterly and monthly summaries

### ✅ Data Management
- CSV import functionality
- Database optimization
- Data validation and processing

### ✅ User Experience
- Dark/Light theme support
- Responsive design
- Intuitive navigation
- Professional UI/UX

## � Development

### Adding New Features
1. Create models in `core/models.py`
2. Update views in `core/views.py`
3. Add URL routes in `core/urls.py`
4. Create templates in `core/templates/`
5. Add static files in `core/static/assets/`

### Running Tests
```bash
python manage.py test
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📊 Data Flow

1. **Data Import**: CSV files → Django management command → Database
2. **API Layer**: Views process database queries → JSON responses
3. **Frontend**: JavaScript fetches API data → Chart.js visualization
4. **User Interface**: Django templates render with context data

## 🔧 Configuration

Key settings in `backend/settings.py`:
- Database configuration
- Static files handling
- Template directories
- Installed applications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Vortex Infinite** - *Initial work* - [GitHub](https://github.com/Vortex-Infinite)

## 🔮 Future Enhancements

- [ ] Advanced analytics and predictions
- [ ] Real-time data streaming
- [ ] Export functionality (PDF, Excel)
- [ ] Mobile application
- [ ] Advanced user management
- [ ] Integration with external APIs

---

**Powered by Django & ORBIS Analytics** © 2025