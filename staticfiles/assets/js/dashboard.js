document.addEventListener('DOMContentLoaded', function() {
    // Initialize all dashboard components
    initTheme();
    initSidebar();
    initProfileDropdown();
    initCharts();
    initLiveClock();
    initNotifications();
    
    // No need for formatCurrencyValues since template handles it now
    
    // Theme Management (Same as login/index pages)
    function initTheme() {
        const themeCheckbox = document.getElementById('theme-checkbox');
        
        const applyTheme = (theme) => {
            document.body.classList.toggle('dark-mode', theme === 'dark-mode');
            if (themeCheckbox) themeCheckbox.checked = (theme === 'dark-mode');
            localStorage.setItem('theme', theme);
        };

        // Check for saved theme, if none, check system preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            applyTheme(savedTheme);
        } else {
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            applyTheme(prefersDark ? 'dark-mode' : 'light-mode');
        }

        if (themeCheckbox) {
            themeCheckbox.addEventListener('change', () => {
                const newTheme = themeCheckbox.checked ? 'dark-mode' : 'light-mode';
                applyTheme(newTheme);
            });
        }
    }
    
    // Sidebar functionality
    function initSidebar() {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebar-toggle');
        
        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', function() {
                sidebar.classList.toggle('collapsed');
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            });
        }
        
        // Restore sidebar state
        if (localStorage.getItem('sidebarCollapsed') === 'true') {
            sidebar?.classList.add('collapsed');
        }
        
        // Navigation items
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                navItems.forEach(nav => nav.classList.remove('active'));
                this.classList.add('active');
                
                // Handle page navigation
                const page = this.dataset.page;
                handlePageNavigation(page);
            });
        });
    }
    
    // Profile dropdown functionality
    function initProfileDropdown() {
        const profileBtn = document.getElementById('profile-btn');
        const profileDropdown = document.getElementById('profile-dropdown');
        const logoutBtn = document.getElementById('logout-btn');
        
        if (profileBtn && profileDropdown) {
            profileBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                profileDropdown.classList.toggle('active');
            });
            
            document.addEventListener('click', function() {
                profileDropdown.classList.remove('active');
            });
            
            profileDropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
        
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function() {
                if (confirm('Are you sure you want to sign out?')) {
                    // Simple redirect to logout - no localStorage manipulation needed
                    window.location.href = '/logout/';
                }
            });
        }
    }
    
    // Initialize charts
    function initCharts() {
        const chartCanvas = document.getElementById('revenueChart');
        if (chartCanvas) {
            const ctx = chartCanvas.getContext('2d');
            
            // Get dynamic data from Django template
            let chartData = [];
            let chartLabels = [];
            
            // Check if trend_data is available from Django
            if (typeof trendData !== 'undefined' && trendData) {
                try {
                    const data = JSON.parse(trendData);
                    chartData = data.map(item => item.revenue);
                    // Add "25" to month labels in frontend
                    chartLabels = data.map(item => {
                        const month = item.month;
                        if (month === 'Jan' || month === 'Feb' || month === 'Mar') {
                            return month + ' 26'; // For 2026 months
                        } else {
                            return month + ' 25'; // For 2025 months
                        }
                    });
                } catch (e) {
                    console.error('Error parsing trend data:', e);
                    // Fallback to static data if parsing fails
                    chartData = [650000, 720000, 680000, 750000, 820000, 790000, 850000, 847392];
                    chartLabels = ['Jan 25', 'Feb 25', 'Mar 25', 'Apr 25', 'May 25', 'Jun 25', 'Jul 25', 'Aug 25'];
                }
            } else {
                // Fallback to static data if no Django data
                chartData = [650000, 720000, 680000, 750000, 820000, 790000, 850000, 847392];
                chartLabels = ['Jan 25', 'Feb 25', 'Mar 25', 'Apr 25', 'May 25', 'Jun 25', 'Jul 25', 'Aug 25'];
            }
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartLabels,
                    datasets: [{
                        label: 'Monthly Revenue (FY 2025-26)',
                        data: chartData,
                        borderColor: getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim(),
                        backgroundColor: 'rgba(66, 153, 225, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim(),
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return 'Monthly Revenue: ₹' + context.parsed.y.toLocaleString('en-IN');
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim()
                            }
                        },
                        y: {
                            display: true,
                            grid: {
                                color: getComputedStyle(document.documentElement).getPropertyValue('--border-color').trim()
                            },
                            ticks: {
                                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim(),
                                callback: function(value) {
                                    return '₹' + value.toLocaleString('en-IN');
                                }
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        }
    }
    
    // Live clock functionality
    function initLiveClock() {
        const timeElement = document.getElementById('live-time');
        
        function updateClock() {
            if (timeElement) {
                const now = new Date();
                const options = {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: true
                };
                timeElement.textContent = now.toLocaleTimeString('en-US', options);
            }
        }
        
        updateClock();
        setInterval(updateClock, 1000);
    }
    
    // Notification functionality  
    function initNotifications() {
        const notificationBtn = document.querySelector('.notification-btn');
        
        if (notificationBtn) {
            notificationBtn.addEventListener('click', function() {
                showNotification('You have 3 new notifications', 'info');
            });
        }
    }
    
    // Page navigation handler
    function handlePageNavigation(page) {
        console.log('Navigate to:', page);
        
        // Add your page navigation logic here
        const actions = {
            'dashboard': () => console.log('Dashboard selected'),
            'analytics': () => showNotification('Analytics page - Coming soon!', 'info'),
            'reports': () => showNotification('Reports page - Coming soon!', 'info'),
            'projects': () => showNotification('Projects page - Coming soon!', 'info'),
            'finance': () => showNotification('Finance page - Coming soon!', 'info'),
            'clients': () => showNotification('Clients page - Coming soon!', 'info'),
            'performance': () => showNotification('Performance page - Coming soon!', 'info'),
            'documents': () => window.location.href = '/document/',
            'settings': () => showNotification('Settings page - Coming soon!', 'info')
        };
        
        if (actions[page]) {
            actions[page]();
        }
    }
    
    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Add notification styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--card-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 8px 25px var(--shadow-color);
            z-index: 1000;
            max-width: 300px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.style.cssText = `
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 4px;
            margin-left: 12px;
        `;
        
        const content = notification.querySelector('.notification-content');
        content.style.cssText = `
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-primary);
            font-size: 14px;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove after 4 seconds
        const autoRemove = setTimeout(() => {
            removeNotification(notification);
        }, 4000);
        
        // Manual close
        closeBtn.addEventListener('click', () => {
            clearTimeout(autoRemove);
            removeNotification(notification);
        });
    }
    
    function removeNotification(notification) {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
    
    // Quick action buttons
    const quickActionBtns = document.querySelectorAll('.quick-action-btn');
    quickActionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const btnText = this.textContent.trim();
            showNotification(`${btnText} - Feature coming soon!`, 'info');
        });
    });
    
    // Animate metrics on page load
    animateMetrics();
    
    function animateMetrics() {
        const metricValues = document.querySelectorAll('.metric-value');
        
        metricValues.forEach((element, index) => {
            const finalValue = element.textContent;
            const isPercentage = finalValue.includes('%');
            const isRupee = finalValue.includes('₹');
            
            let numericValue;
            if (isRupee) {
                numericValue = parseFloat(finalValue.replace(/[₹,]/g, ''));
            } else {
                numericValue = parseFloat(finalValue.replace(/[^0-9.]/g, ''));
            }
            
            let currentValue = 0;
            const increment = numericValue / 50;
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= numericValue) {
                    currentValue = numericValue;
                    clearInterval(timer);
                }
                
                if (isRupee) {
                    element.textContent = '₹' + Math.floor(currentValue).toLocaleString('en-IN');
                } else if (isPercentage) {
                    element.textContent = currentValue.toFixed(1) + '%';
                } else {
                    element.textContent = Math.floor(currentValue);
                }
            }, 20);
            
            // Delay animation for each metric
            setTimeout(() => {
                // Animation starts automatically
            }, index * 200);
        });
    }
    
    console.log('Professional Dashboard initialized successfully');
});
