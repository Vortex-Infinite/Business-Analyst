document.addEventListener('DOMContentLoaded', () => {
    // --- UNIVERSAL LOGIC ---
    handleTheme();

    // --- PAGE-SPECIFIC LOGIC ---
    if (document.body.classList.contains('dashboard-page')) {
        Dashboard.init();
    } else {
        LoginPage.init();
    }
});

// --- THEME MANAGEMENT ---
function handleTheme() {
    const themeCheckbox = document.getElementById('theme-checkbox');
    const applyTheme = (theme) => {
        document.body.classList.toggle('dark-mode', theme === 'dark-mode');
        if (themeCheckbox) themeCheckbox.checked = (theme === 'dark-mode');
    };
    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark-mode' : 'light-mode');
    applyTheme(savedTheme);

    if (themeCheckbox) {
        themeCheckbox.addEventListener('change', () => {
            const newTheme = themeCheckbox.checked ? 'dark-mode' : 'light-mode';
            localStorage.setItem('theme', newTheme);
            applyTheme(newTheme);
        });
    }
}

// --- LOGIN PAGE LOGIC ---
const LoginPage = {
    init() {
        const employeeLoginForm = document.getElementById('employee-login-form');
        const hrLoginForm = document.getElementById('hr-login-form');
        if (employeeLoginForm) this.attachEmployeeLoginListener(employeeLoginForm);
        if (hrLoginForm) this.attachHrLoginListeners(hrLoginForm);
    },
    async handleLogin(email, password, role) {
        // ... (login logic from previous version)
    },
    // ... (rest of login listeners)
};

// --- DASHBOARD LOGIC (UNIFIED) ---
const Dashboard = {
    state: {
        user: { name: 'Gowshik S.', email: 'hr@abcinc.com', avatar: 'https://randomuser.me/api/portraits/men/87.jpg' },
        isSidebarCollapsed: false,
    },
    
    init() {
        // Render all dashboard components
        this.renderSidebar();
        this.renderHeader();
        this.renderMainContent();

        // Attach all event listeners
        this.attachEventListeners();
    },

    renderSidebar() {
        const sidebar = document.getElementById('sidebar');
        if (!sidebar) return;
        sidebar.innerHTML = `
            <div class="sidebar-header"><h1 class="sidebar-logo">FinPulse AI</h1></div>
            <nav class="sidebar-nav">
                <a href="#" class="nav-item active"><i class="fas fa-chart-pie"></i><span>Overview</span></a>
                <a href="#" class="nav-item"><i class="fas fa-dollar-sign"></i><span>Revenue</span></a>
                <a href="#" class="nav-item"><i class="fas fa-receipt"></i><span>Expenses</span></a>
                <a href="#" class="nav-item"><i class="fas fa-chart-line"></i><span>Forecasts</span></a>
            </nav>
            <div class="sidebar-footer">
                <button class="sidebar-toggle" id="sidebar-toggle">
                    <i class="fas fa-chevron-left"></i><span>Collapse</span>
                </button>
            </div>`;
    },

    renderHeader() {
        const header = document.getElementById('dashboard-header');
        if (!header) return;
        header.innerHTML = `
            <div class="header-title">Good morning, ${this.state.user.name.split(' ')[0]}! <span id="live-time"></span></div>
            <div class="header-actions">
                <button class="profile-btn" id="profile-btn">
                    <img src="${this.state.user.avatar}" alt="Profile">
                </button>
                <div class="profile-dropdown" id="profile-dropdown">
                    </div>
            </div>`;
    },

    renderMainContent() {
        const main = document.getElementById('main-content');
        if (!main) return;
        main.innerHTML = `
            <div class="dash-grid">
                <div class="widget"><div class="title">Monthly Revenue</div><div class="financial-metric success">+₹1,50,000</div><p class="widget-subtitle">Up 15% from last month</p></div>
                <div class="widget"><div class="title">Monthly Expenses</div><div class="financial-metric error">-₹85,000</div><p class="widget-subtitle">Down 5% from last month</p></div>
                <div class="widget"><div class="title">Net Cash Flow</div><div class="financial-metric">+₹65,000</div><p class="widget-subtitle">Healthy cash position</p></div>
                <div class="widget"><div class="title">🚨 AI Anomaly Alert</div><div class="inbox-msg"><b>Unusual Spending Spike:</b> ₹15,000 on 'Software'.<br><span>(Typically ₹2,000/week)</span></div></div>
            </div>`;
    },

    attachEventListeners() {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebar-toggle');
        
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
                this.state.isSidebarCollapsed = !this.state.isSidebarCollapsed;
            });
        }
        
        // Live Clock
        const timeElement = document.getElementById('live-time');
        const updateClock = () => {
            if (timeElement) timeElement.textContent = new Date().toLocaleTimeString('en-US');
        };
        setInterval(updateClock, 1000);
        updateClock();

        // ... (attach listeners for profile dropdown, logout, etc.)
    }
};