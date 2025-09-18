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
    
    // Theme Management (Same as existing)
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
                            window.location.href = '/logout/';
                        }, 1500);
                    } catch (error) {
                        console.error('Logout error:', error);
                    }
                }
            });
        }
    }
    
    // Advanced Notification System for CEO
    function initNotificationSystem() {
        const notificationBtn = document.getElementById('notification-btn');
        const notificationDropdown = document.getElementById('notification-dropdown');
        const markAllReadBtn = document.getElementById('mark-all-read');
        const notificationCount = document.getElementById('notification-count');
        
        if (notificationBtn && notificationDropdown) {
            notificationBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                notificationDropdown.classList.toggle('active');
                updateNotificationDisplay();
            });
            
            document.addEventListener('click', function() {
                notificationDropdown.classList.remove('active');
            });
            
            notificationDropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
        
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', function() {
                markAllNotificationsAsRead();
            });
        }
        
        // Handle notification actions
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('approve-btn')) {
                handleNotificationAction(e.target, 'approve');
            } else if (e.target.classList.contains('review-btn')) {
                handleNotificationAction(e.target, 'review');
            }
        });
        
        // Initialize notification count
        updateNotificationCount();
    }
    
    // Analyst Notification System
    function initAnalystNotifications() {
        // Simulate receiving notifications from analysts
        setInterval(() => {
            if (Math.random() > 0.97) { // 3% chance every interval
                receiveAnalystNotification();
            }
        }, 30000); // Check every 30 seconds
        
        // Load existing analyst notifications
        loadAnalystNotifications();
    }
    
    function receiveAnalystNotification() {
        const notifications = [
            {
                type: 'analyst-publish',
                title: 'Financial Report Published',
                text: 'Q3 Financial Analysis has been published and requires CEO review',
                analyst: 'Financial Analyst',
                time: 'Just now'
            },
            {
                type: 'analyst-confirm',
                title: 'Market Research Confirmed',
                text: 'Market expansion study has been confirmed - Strategic decision required',
                analyst: 'Market Analyst',
                time: 'Just now'
            },
            {
                type: 'analyst-publish',
                title: 'Risk Assessment Complete',
                text: 'Comprehensive risk assessment published - Executive approval needed',
                analyst: 'Risk Analyst',
                time: 'Just now'
            }
        ];
        
        const notification = notifications[Math.floor(Math.random() * notifications.length)];
        addNotificationToUI(notification);
        showExecutiveNotification(`New ${notification.title} from ${notification.analyst}`, 'info');
        updateNotificationCount();
    }
    
    function addNotificationToUI(notification) {
        const notificationList = document.getElementById('notification-list');
        if (!notificationList) return;
        
        const notificationHTML = `
            <div class="notification-item unread analyst-notification" data-type="${notification.type}">
                <div class="notification-icon">
                    <i class="fas fa-${notification.type === 'analyst-publish' ? 'file-alt' : 'check-circle'}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">${notification.title}</div>
                    <div class="notification-text">${notification.text}</div>
                    <div class="notification-time">${notification.time}</div>
                </div>
                <div class="notification-actions">
                    <button class="approve-btn" data-action="approve">Approve</button>
                    <button class="review-btn" data-action="review">Review</button>
                </div>
            </div>
        `;
        
        notificationList.insertAdjacentHTML('afterbegin', notificationHTML);
    }
    
    function handleNotificationAction(button, action) {
        const notificationItem = button.closest('.notification-item');
        const title = notificationItem.querySelector('.notification-title').textContent;
        
        if (action === 'approve') {
            notificationItem.style.opacity = '0.6';
            showExecutiveNotification(`Approved: ${title}`, 'success');
            setTimeout(() => {
                notificationItem.remove();
                updateNotificationCount();
            }, 1000);
        } else if (action === 'review') {
            showExecutiveNotification(`Marked for review: ${title}`, 'info');
            notificationItem.classList.remove('unread');
            updateNotificationCount();
        }
    }
    
    function markAllNotificationsAsRead() {
        const unreadNotifications = document.querySelectorAll('.notification-item.unread');
        unreadNotifications.forEach(notification => {
            notification.classList.remove('unread');
        });
        updateNotificationCount();
        showExecutiveNotification('All notifications marked as read', 'success');
    }
    
    function updateNotificationCount() {
        const unreadCount = document.querySelectorAll('.notification-item.unread').length;
        const notificationCount = document.getElementById('notification-count');
        
        if (notificationCount) {
            notificationCount.textContent = unreadCount;
            notificationCount.style.display = unreadCount > 0 ? 'flex' : 'none';
        }
        
        // Update sidebar notification count
        const sidebarNotificationCount = document.querySelector('.notification-count');
        if (sidebarNotificationCount) {
            const pendingApprovals = document.querySelectorAll('.analyst-notification.unread').length;
            sidebarNotificationCount.textContent = pendingApprovals;
            sidebarNotificationCount.style.display = pendingApprovals > 0 ? 'block' : 'none';
        }
    }
    
    function updateNotificationDisplay() {
        // Sort notifications by time and unread status
        const notificationList = document.getElementById('notification-list');
        if (!notificationList) return;
        
        const notifications = Array.from(notificationList.children);
        notifications.sort((a, b) => {
            const aUnread = a.classList.contains('unread');
            const bUnread = b.classList.contains('unread');
            
            if (aUnread && !bUnread) return -1;
            if (!aUnread && bUnread) return 1;
            return 0;
        });
        
        notifications.forEach(notification => {
            notificationList.appendChild(notification);
        });
    }
    
    function loadAnalystNotifications() {
        // Load any stored notifications from localStorage
        const storedNotifications = localStorage.getItem('ceoNotifications');
        if (storedNotifications) {
            const notifications = JSON.parse(storedNotifications);
            notifications.forEach(notification => {
                addNotificationToUI(notification);
            });
        }
        updateNotificationCount();
    }
    
    // Executive Actions System
    function initExecutiveActions() {
        const actionButtons = document.querySelectorAll('.action-controls .approve-btn, .action-controls .review-btn');
        
        actionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const actionItem = this.closest('.action-item');
                const actionTitle = actionItem.querySelector('.action-title').textContent;
                const isApprove = this.classList.contains('approve-btn');
                
                if (isApprove) {
                    handleExecutiveApproval(actionItem, actionTitle);
                } else {
                    handleExecutiveReview(actionItem, actionTitle);
                }
            });
        });
    }
    
    function handleExecutiveApproval(actionItem, title) {
        actionItem.style.opacity = '0.6';
        showExecutiveNotification(`Approved: ${title}`, 'success');
        
        setTimeout(() => {
            actionItem.style.display = 'none';
            updateUrgencyCounter();
        }, 1500);
    }
    
    function handleExecutiveReview(actionItem, title) {
        showExecutiveNotification(`Marked for detailed review: ${title}`, 'info');
        actionItem.classList.add('under-review');
        actionItem.style.opacity = '0.8';
    }
    
    function updateUrgencyCounter() {
        const visibleActions = document.querySelectorAll('.action-item:not([style*="display: none"])').length;
        const urgencyCount = document.querySelector('.urgency-count');
        
        if (urgencyCount) {
            urgencyCount.textContent = visibleActions;
        }
    }
    
    // Enhanced Charts for CEO
    function initCharts() {
        const chartCanvas = document.getElementById('revenueAnalysisChart');
        if (chartCanvas) {
            const ctx = chartCanvas.getContext('2d');
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025 (Proj)'],
                    datasets: [
                        {
                            label: 'Revenue',
                            data: [38500000, 41200000, 39900000, 45300000, 42800000, 46100000, 47200000, 51000000],
                            borderColor: '#4299e1',
                            backgroundColor: 'rgba(66, 153, 225, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointBackgroundColor: '#4299e1',
                            pointBorderColor: '#ffffff',
                            pointBorderWidth: 2,
                            pointRadius: 6,
                            pointHoverRadius: 8
                        },
                        {
                            label: 'Profit',
                            data: [9500000, 10100000, 9800000, 11200000, 10600000, 11400000, 11700000, 12600000],
                            borderColor: '#48bb78',
                            backgroundColor: 'rgba(72, 187, 120, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointBackgroundColor: '#48bb78',
                            pointBorderColor: '#ffffff',
                            pointBorderWidth: 2,
                            pointRadius: 6,
                            pointHoverRadius: 8
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                usePointStyle: true,
                                padding: 20,
                                font: {
                                    family: 'Poppins',
                                    size: 14,
                                    weight: '600'
                                }
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: {
                                family: 'Poppins',
                                size: 14,
                                weight: '600'
                            },
                            bodyFont: {
                                family: 'Poppins',
                                size: 13
                            },
                            cornerRadius: 8,
                            displayColors: true,
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': $' + context.parsed.y.toLocaleString();
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
                <i class="fas fa-info-circle"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
});
