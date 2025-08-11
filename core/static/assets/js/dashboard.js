// HR Dashboard page component
window.DashboardPage = {
    // --- STATE MANAGEMENT ---
    clockInState: {
        status: 'Clocked Out', // 'Clocked Out', 'Clocked In', 'On Break'
        clockInTime: null,
        breakStartTime: null,
        timerInterval: null
    },

    init() {
        // Load saved state from localStorage
        const savedState = localStorage.getItem('clockInState');
        if (savedState) {
            this.clockInState = JSON.parse(savedState);
        }
        this.render();
    },

    render() {
        document.getElementById('root').innerHTML = `
            <div class="dashboard-container">
                <div class="sidebar" id="sidebar">
                    <div class="sidebar-logo">
                        <h2>${CONFIG.COMPANY_BRAND}</h2>
                        <button class="sidebar-toggle-btn-internal" id="sidebar-toggle">
                            <i class="fas fa-bars"></i>
                        </button>
                    </div>
                    <div class="sidebar-section">
                        <div class="sidebar-section-title">Main</div>
                        <button class="sidebar-menu-item active">
                            <i class="fas fa-home"></i>
                            <span>Dashboard</span>
                        </button>
                        <button class="sidebar-menu-item">
                            <i class="fas fa-users"></i>
                            <span>Employees</span>
                        </button>
                        <button class="sidebar-menu-item">
                            <i class="fas fa-calendar-alt"></i>
                            <span>Schedule</span>
                        </button>
                    </div>
                    <div class="sidebar-section">
                        <div class="sidebar-section-title">HR</div>
                            <button class="sidebar-menu-item" id="goToReport">
                                <i class="fas fa-file-contract"></i>
                                <span>Reports</span>
                            </button>
                        <button class="sidebar-menu-item">
                            <i class="fas fa-cog"></i>
                            <span>Settings</span>
                        </button>
                    </div>
                </div>
                <div class="dashboard-main">
                    <div class="dash-header">
                        <div class="dash-greeting">
                            <b>Good ${this.getTimeGreeting()}, HR Manager!</b>
                            <div style="font-size: 14px; color: var(--text-secondary); margin-top: 5px;">
                                ${this.getCurrentDate()}
                            </div>
                        </div>
                        <div class="header-actions">
                            <button class="profile-btn" id="profile-btn">
                                <img src="https://via.placeholder.com/40x40/5D3EBC/ffffff?text=HR" alt="Profile">
                                <span>HR Manager</span>
                                <i class="fas fa-chevron-down"></i>
                            </button>
                            <div class="profile-dropdown" id="profile-dropdown">
                                <div class="dropdown-header">
                                    <div class="name">HR Manager</div>
                                    <div class="email">hr@${CONFIG.COMPANY_BRAND.toLowerCase().replace(' ', '')}.com</div>
                                </div>
                                <div class="dropdown-section">
                                    <a href="#" class="dropdown-item">
                                        <i class="fas fa-user"></i>
                                        Profile Settings
                                    </a>
                                    <a href="#" class="dropdown-item">
                                        <i class="fas fa-bell"></i>
                                        Notifications
                                    </a>
                                    <a href="#" class="dropdown-item">
                                        <i class="fas fa-bell"></i>
                                        Dark Mode   
                                    </a>
                                </div>
                                <div class="dropdown-section">
                                    <a href="#" class="dropdown-item" onclick="DashboardPage.logout()">
                                        <i class="fas fa-sign-out-alt"></i>
                                        Logout
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="dash-grid">
                        <div class="widget clock-in-widget-container">
                        </div>
                        <div class="widget">
                            <div class="title">Recent Activity</div>
                            <div class="inbox-msg">Employee John Doe clocked in at 9:00 AM</div>
                            <div class="inbox-msg">New leave request from Jane Smith</div>
                            <div class="inbox-msg">Payroll processing completed</div>
                        </div>
                        <div class="widget">
                            <div class="title">Today's Schedule</div>
                            <div class="event">Team Meeting - 10:00 AM</div>
                            <div class="event">Performance Review - 2:00 PM</div>
                            <div class="event">HR Planning Session - 4:00 PM</div>
                        </div>
                        <div class="widget">
                            <div class="title">Quick Stats</div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                                <div style="text-align: center;">
                                    <div style="font-size: 24px; font-weight: 600; color: var(--success);">24</div>
                                    <div style="font-size: 12px; color: var(--text-secondary);">Employees Present</div>
                                </div>
                                <div style="text-align: center;">
                                    <div style="font-size: 24px; font-weight: 600; color: var(--warning);">3</div>
                                    <div style="font-size: 12px; color: var(--text-secondary);">Pending Requests</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        // Initial render of the clock-in widget and other components
        this.updateClockInWidget();
        this.initializeInteractions();
    },

    // --- CLOCK-IN WIDGET LOGIC ---
    updateClockInWidget() {
        const container = document.querySelector('.clock-in-widget-container');
        if (!container) return;

        let statusText = this.clockInState.status.replace(/([A-Z])/g, ' $1').trim();
        let buttonHTML = '';
        let timerText = '00:00:00';

        switch (this.clockInState.status) {
            case 'Clocked Out':
                buttonHTML = `<button class="btn btn-clock-in" onclick="DashboardPage.handleClockIn()">Clock In</button>`;
                break;
            case 'Clocked In':
                buttonHTML = `
                    <button class="btn btn-start-break" onclick="DashboardPage.handleStartBreak()">Start Break</button>
                    <button class="btn btn-clock-out" onclick="DashboardPage.handleClockOut()">Clock Out</button>
                `;
                break;
            case 'On Break':
                 statusText = 'On Break';
                buttonHTML = `<button class="btn btn-end-break" onclick="DashboardPage.handleEndBreak()">End Break</button>`;
                break;
        }
        
        container.innerHTML = `
            <div class="title">Time Tracking</div>
            <div class="clock-in-widget">
                <div class="status-text">${statusText}</div>
                <div class="timer" id="clock-in-timer">${timerText}</div>
                <div class="widget-buttons">${buttonHTML}</div>
            </div>
        `;

        this.startTimer();
    },
    
    startTimer() {
        if (this.clockInState.timerInterval) clearInterval(this.clockInState.timerInterval);
        const timerElement = document.getElementById('clock-in-timer');
        if (!timerElement) return;

        const startTime = this.clockInState.status === 'On Break' ? this.clockInState.breakStartTime : this.clockInState.clockInTime;

        if (!startTime) {
            timerElement.textContent = '00:00:00';
            return;
        }
        
        this.clockInState.timerInterval = setInterval(() => {
            const now = new Date();
            const start = new Date(startTime);
            const diff = now - start;

            let seconds = Math.floor((diff / 1000) % 60);
            let minutes = Math.floor((diff / (1000 * 60)) % 60);
            let hours = Math.floor(diff / (1000 * 60 * 60));

            hours = String(hours).padStart(2, '0');
            minutes = String(minutes).padStart(2, '0');
            seconds = String(seconds).padStart(2, '0');
            
            timerElement.textContent = `${hours}:${minutes}:${seconds}`;
        }, 1000);
    },

    // --- EVENT HANDLERS ---
    handleClockIn() {
        this.clockInState.status = 'Clocked In';
        this.clockInState.clockInTime = new Date().toISOString();
        this.saveStateAndRerender();
    },
    handleStartBreak() {
        this.clockInState.status = 'On Break';
        this.clockInState.breakStartTime = new Date().toISOString();
        this.saveStateAndRerender();
    },
    handleEndBreak() {
        this.clockInState.status = 'Clocked In';
        this.clockInState.breakStartTime = null; // Reset break time
        this.saveStateAndRerender();
    },
    handleClockOut() {
        if (confirm('Are you sure you want to clock out?')) {
            this.clockInState.status = 'Clocked Out';
            this.clockInState.clockInTime = null;
            this.clockInState.breakStartTime = null;
            if (this.clockInState.timerInterval) clearInterval(this.clockInState.timerInterval);
            this.clockInState.timerInterval = null;
            this.saveStateAndRerender();
        }
    },
    
    saveStateAndRerender() {
        localStorage.setItem('clockInState', JSON.stringify(this.clockInState));
        this.updateClockInWidget();
    },
    
    // --- HELPER METHODS ---
    getTimeGreeting() {
        const hour = new Date().getHours();
        if (hour < 12) return 'Morning';
        if (hour < 17) return 'Afternoon';
        return 'Evening';
    },

    getCurrentDate() {
        const now = new Date();
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        return now.toLocaleDateString('en-US', options);
    },

    // --- INTERACTION HANDLERS ---
    initializeInteractions() {
        // Sidebar toggle functionality
        document.getElementById('sidebar-toggle')?.addEventListener('click', () => {
            this.toggleSidebar();
        });

        // Profile dropdown toggle
        document.getElementById('profile-btn')?.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleProfileDropdown();
        });
            document.getElementById('goToReport').onclick = function() {
                window.location.href = 'document.html'; // Redirect to the correct report page
            };

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            const dropdown = document.getElementById('profile-dropdown');
            const profileBtn = document.getElementById('profile-btn');
            if (dropdown && !profileBtn?.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
        // Example for a menu item with data-menu="report"
document.querySelectorAll('.sidebar-menu-item').forEach(function(btn){
    btn.addEventListener('click', function(){
        const menu = btn.getAttribute('data-menu');
        if(menu === 'report'){
            window.location.href = 'report.html'; // Adjust filename as needed
        }
        // ...existing code...
    });
});
        // Menu item interactions
        document.querySelectorAll('.sidebar-menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                this.handleMenuItemClick(e.target.closest('.sidebar-menu-item'));
            });
        });
    },

    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        if (!sidebar) return;
        
        sidebar.classList.toggle('collapsed');
        
        // Update toggle icon
        const toggleBtn = document.getElementById('sidebar-toggle');
        const icon = toggleBtn?.querySelector('i');
        if (icon) {
            if (sidebar.classList.contains('collapsed')) {
                icon.className = 'fas fa-bars';
            } else {
                icon.className = 'fas fa-times';
            }
        }
    },

    toggleProfileDropdown() {
        const dropdown = document.getElementById('profile-dropdown');
        if (dropdown) {
            dropdown.classList.toggle('active');
        }
    },

    handleMenuItemClick(menuItem) {
        if (!menuItem) return;
        
        // Remove active class from all menu items
        document.querySelectorAll('.sidebar-menu-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Add active class to clicked item
        menuItem.classList.add('active');
        
        // Get the menu item text for potential navigation
        const menuText = menuItem.querySelector('span')?.textContent;
        console.log(`Navigating to: ${menuText}`);
        
        // Here you could implement actual navigation logic
        // For now, we'll just log the action
    },

   // ...existing code...
logout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear any stored session data
        localStorage.removeItem('currentUser'); // <-- Add this line
        localStorage.removeItem('user');
        localStorage.removeItem('theme');
        // Redirect to login page
        window.location.href = '../auth/hr_login.html';
    }
}
// ...existing code...
};

// Initial render when the script loads
DashboardPage.init();