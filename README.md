# Project Structure: Business Analyst Platform

## 📁 File Organization

/Business-Analyst/
│
├── 📄 manage.py                # Django's command-line utility
│
├── 📁 backend/                  # The main Django project folder
│   ├── 📄 settings.py          # Project settings (INSTALLED_APPS, DB, etc.)
│   ├── 📄 urls.py              # Main URL router for the project
│   └── ... (other config files)
│
└── 📁 core/                     # The primary application
    ├── 📄 models.py             # Database models
    ├── 📄 views.py              # Request handling logic
    ├── 📄 urls.py               # App-specific URL routes
    ├── 📁 static/               # Holds all frontend assets (CSS, JS)
    └── 📁 templates/            # Holds all frontend HTML files