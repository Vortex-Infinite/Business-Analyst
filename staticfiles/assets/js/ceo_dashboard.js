document.addEventListener('DOMContentLoaded', function() {
    // Initialize all CEO dashboard components
    initTheme();
    initSidebar();
    initProfileDropdown();
    initNotificationSystem();
    initCharts();
    initLiveClock();
    initAnalystNotifications();
    initExecutiveActions();
    
    // Theme Management
    function initTheme() {
        const themeCheckbox = document.getElementById('theme-checkbox');
        
        const applyTheme = (theme) => {
            document.body.classList.toggle('dark-mode', theme === 'dark-mode');
            if (themeCheckbox) themeCheckbox.checked = (theme === 'dark-mode');
            localStorage.setItem('theme', theme);
        };

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
    
    // Sidebar functionality (Enhanced for CEO)
    function initSidebar() {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebar-toggle');
        
        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', function() {
                sidebar.classList.toggle('collapsed');
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            });
        }
        
        if (localStorage.getItem('sidebarCollapsed') === 'true') {
            sidebar?.classList.add('collapsed');
        }
        
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                navItems.forEach(nav => nav.classList.remove('active'));
                this.classList.add('active');
                
                const page = this.dataset.page;
                handleCEOPageNavigation(page);
            });
        });
    }
    
    // Enhanced Profile Dropdown
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
            logoutBtn.addEventListener('click', async function() {
                if (confirm('Are you sure you want to sign out from the Executive Dashboard?')) {
                    try {
                        localStorage.removeItem('currentUser');
                        localStorage.removeItem('theme');
                        showExecutiveNotification('Secure logout completed', 'success');
                        setTimeout(() => {
                            window.location.href = '/';
                        }, 1500);
                    } catch (error) {
                        console.error('Logout error:', error);
                    }
                }
            });
        }
    }
    
    // Enhanced Notification System for CEO
    function initNotificationSystem() {
        const notificationBtn = document.querySelector('.notification-btn');
        const notificationBadge = document.querySelector('.notification-badge');
        
        if (notificationBtn) {
            notificationBtn.addEventListener('click', function() {
                showExecutiveNotification('Notifications panel opened', 'info');
            });
        }
        
        // Update notification count
        if (notificationBadge) {
            updateNotificationCount();
        }
    }
    
    // Analyst Notifications for CEO
    function initAnalystNotifications() {
        // Simulate receiving analyst notifications
        setInterval(() => {
            if (Math.random() > 0.7) {
                receiveAnalystNotification();
            }
        }, 30000); // Every 30 seconds
    }
    
    function receiveAnalystNotification() {
        const notifications = [
            'New market analysis report available',
            'Financial forecast updated',
            'Risk assessment completed',
            'Competitive analysis ready',
            'Performance metrics updated'
        ];
        
        const randomNotification = notifications[Math.floor(Math.random() * notifications.length)];
        addNotificationToUI({
            id: Date.now(),
            message: randomNotification,
            type: 'info',
            timestamp: new Date(),
            read: false
        });
    }
    
    function addNotificationToUI(notification) {
        const notificationContainer = document.querySelector('.notifications-container');
        if (!notificationContainer) return;
        
        const notificationElement = document.createElement('div');
        notificationElement.className = `notification-item ${notification.type} ${notification.read ? 'read' : 'unread'}`;
        notificationElement.innerHTML = `
            <div class="notification-content">
                <div class="notification-message">${notification.message}</div>
                <div class="notification-time">${notification.timestamp.toLocaleTimeString()}</div>
            </div>
            <div class="notification-actions">
                <button class="action-btn view" onclick="handleNotificationAction(this, 'view')">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="action-btn dismiss" onclick="handleNotificationAction(this, 'dismiss')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        notificationContainer.appendChild(notificationElement);
        updateNotificationCount();
    }
    
    function handleNotificationAction(button, action) {
        const notificationItem = button.closest('.notification-item');
        
        if (action === 'view') {
            showExecutiveNotification('Opening detailed view...', 'info');
            notificationItem.classList.add('read');
        } else if (action === 'dismiss') {
            notificationItem.remove();
        }
        
        updateNotificationCount();
    }
    
    function markAllNotificationsAsRead() {
        const unreadNotifications = document.querySelectorAll('.notification-item.unread');
        unreadNotifications.forEach(notification => {
            notification.classList.remove('unread');
            notification.classList.add('read');
        });
        updateNotificationCount();
    }
    
    function updateNotificationCount() {
        const notificationBadge = document.querySelector('.notification-badge');
        const unreadCount = document.querySelectorAll('.notification-item.unread').length;
        
        if (notificationBadge) {
            notificationBadge.textContent = unreadCount;
            notificationBadge.style.display = unreadCount > 0 ? 'block' : 'none';
        }
    }
    
    function updateNotificationDisplay() {
        const notifications = document.querySelectorAll('.notification-item');
        notifications.forEach(notification => {
            const timestamp = new Date(notification.dataset.timestamp);
            const timeDiff = Date.now() - timestamp.getTime();
            
            if (timeDiff > 300000) { // 5 minutes
                notification.classList.add('stale');
            }
        });
    }
    
    function loadAnalystNotifications() {
        // Load existing notifications from localStorage or API
        const savedNotifications = localStorage.getItem('ceoNotifications');
        if (savedNotifications) {
            const notifications = JSON.parse(savedNotifications);
            notifications.forEach(notification => {
                addNotificationToUI(notification);
            });
        }
    }
    
    // Executive Actions and Approvals
    function initExecutiveActions() {
        const approvalItems = document.querySelectorAll('.approval-item');
        approvalItems.forEach(item => {
            const approveBtn = item.querySelector('.approve-btn');
            const rejectBtn = item.querySelector('.reject-btn');
            const reviewBtn = item.querySelector('.review-btn');
            
            if (approveBtn) {
                approveBtn.addEventListener('click', () => {
                    handleExecutiveApproval(item, 'Approve');
                });
            }
            
            if (rejectBtn) {
                rejectBtn.addEventListener('click', () => {
                    handleExecutiveApproval(item, 'Reject');
                });
            }
            
            if (reviewBtn) {
                reviewBtn.addEventListener('click', () => {
                    handleExecutiveReview(item, 'Review');
                });
            }
        });
        
        updateUrgencyCounter();
    }
    
    function handleExecutiveApproval(actionItem, title) {
        const itemTitle = actionItem.querySelector('.approval-title').textContent;
        showExecutiveNotification(`${title}: ${itemTitle}`, 'success');
        actionItem.remove();
        updateUrgencyCounter();
    }
    
    function handleExecutiveReview(actionItem, title) {
        const itemTitle = actionItem.querySelector('.approval-title').textContent;
        showExecutiveNotification(`Review requested: ${itemTitle}`, 'info');
    }
    
    function updateUrgencyCounter() {
        const urgencyCounter = document.querySelector('.urgency-counter');
        const approvalItems = document.querySelectorAll('.approval-item');
        
        if (urgencyCounter) {
            urgencyCounter.textContent = approvalItems.length;
        }
    }
    
    // Enhanced Charts for CEO Dashboard
    function initCharts() {
        // Revenue Trend Chart
        const revenueChart = document.getElementById('revenueChart');
        if (revenueChart) {
            const ctx = revenueChart.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Revenue',
                        data: [1200000, 1350000, 1420000, 1580000, 1650000, 1800000],
                        borderColor: getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim(),
                        backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim() + '20',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            grid: {
                                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim(),
                                drawBorder: false
                            },
                            ticks: {
                                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim(),
                                font: {
                                    family: 'Poppins',
                                    size: 12,
                                    weight: '500'
                                }
                            }
                        },
                        y: {
                            display: true,
                            grid: {
                                color: getComputedStyle(document.documentElement).getPropertyValue('--border-color').trim(),
                                drawBorder: false
                            },
                            ticks: {
                                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim(),
                                font: {
                                    family: 'Poppins',
                                    size: 12,
                                    weight: '500'
                                },
                                callback: function(value) {
                                    return '$' + (value / 1000000).toFixed(1) + 'M';
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
    
    // Enhanced Live Clock
    function initLiveClock() {
        const timeElement = document.getElementById('live-time');
        const lastUpdatedElement = document.getElementById('last-updated-time');
        
        function updateClock() {
            if (timeElement) {
                const now = new Date();
                const options = {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: true,
                    timeZoneName: 'short'
                };
                timeElement.textContent = now.toLocaleTimeString('en-US', options);
            }
            
            if (lastUpdatedElement) {
                const now = new Date();
                lastUpdatedElement.textContent = now.toLocaleString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            }
        }
        
        updateClock();
        setInterval(updateClock, 1000);
    }
    
    // CEO Page Navigation
    function handleCEOPageNavigation(page) {
        console.log('CEO Navigate to:', page);
        
        const actions = {
            'dashboard': () => console.log('Executive Dashboard selected'),
            'strategic-analytics': () => showExecutiveNotification('Strategic Analytics - Advanced intelligence loading...', 'info'),
            'approvals': () => showExecutiveNotification('Approvals Hub - 5 pending executive decisions', 'warning'),
            'financial-overview': () => showExecutiveNotification('Financial Overview - Real-time data loading...', 'info'),
            'performance-insights': () => showExecutiveNotification('Performance Insights - Enterprise metrics loading...', 'info'),
            'market-analysis': () => showExecutiveNotification('Market Analysis - Global intelligence updating...', 'info'),
            'competitive-intel': () => showExecutiveNotification('Competitive Intelligence - Confidential data loading...', 'info'),
            'team-performance': () => showExecutiveNotification('Team Performance - Organization-wide metrics loading...', 'info'),
            'project-portfolio': () => showExecutiveNotification('Project Portfolio - Strategic initiatives overview...', 'info'),
            'risk-management': () => showExecutiveNotification('Risk Management - Enterprise risk assessment...', 'warning'),
            'compliance': () => showExecutiveNotification('Compliance Center - Regulatory status checking...', 'info'),
            'board-reports': () => showExecutiveNotification('Board Reports - Executive summaries preparing...', 'info'),
            'strategic-planning': () => showExecutiveNotification('Strategic Planning - Long-term roadmap access...', 'info'),
            'executive-settings': () => showExecutiveNotification('Executive Settings - High-security configuration...', 'info')
        };
        
        if (actions[page]) {
            actions[page]();
        }
    }
    
    // Executive Notification System
    function showExecutiveNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `executive-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Add to notification container
        const container = document.querySelector('.notifications-container') || document.body;
        container.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }
});
        
