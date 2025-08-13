// Transaction Page Specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize transaction page components
    initTransactionRefresh();
    initAnomalyUpdates();
    initNavigation();
    initScrollEffects();
    
    console.log('Transaction page initialized');
    
    // Initialize scroll effects for dynamic sidebar
    function initScrollEffects() {
        const mainWrapper = document.querySelector('.main-wrapper');
        const sidebar = document.querySelector('.sidebar');
        const header = document.querySelector('.dashboard-header');
        
        if (mainWrapper) {
            let scrollTimeout;
            
            mainWrapper.addEventListener('scroll', function() {
                const scrollTop = this.scrollTop;
                
                // Add scrolled class for enhanced shadow
                if (scrollTop > 10) {
                    sidebar?.classList.add('scrolled');
                    header?.classList.add('scrolled');
                } else {
                    sidebar?.classList.remove('scrolled');
                    header?.classList.remove('scrolled');
                }
                
                // Clear existing timeout
                clearTimeout(scrollTimeout);
                
                // Add scrolling class for animations
                document.body.classList.add('scrolling');
                
                // Remove scrolling class after scroll ends
                scrollTimeout = setTimeout(() => {
                    document.body.classList.remove('scrolling');
                }, 150);
            });
        }
        
        // Also handle window scroll for fallback
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > 10) {
                sidebar?.classList.add('scrolled');
                header?.classList.add('scrolled');
            } else {
                sidebar?.classList.remove('scrolled');
                header?.classList.remove('scrolled');
            }
        });
    }
    
    // Initialize navigation for transaction page
    function initNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', function(e) {
                // Only prevent default for items without href or with href="#"
                if (!this.href || this.href.endsWith('#')) {
                    e.preventDefault();
                    navItems.forEach(nav => nav.classList.remove('active'));
                    this.classList.add('active');
                } else {
                    // For items with real URLs, add a loading transition
                    navItems.forEach(nav => nav.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Add a brief transition effect
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        this.style.transform = 'translateX(6px)';
                    }, 150);
                }
            });
        });
    }
    
    // Auto-refresh transaction data
    function initTransactionRefresh() {
        const refreshBtn = document.querySelector('.transaction-box .action-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function() {
                showNotification('Transaction data refreshed', 'success');
                // Here you would typically make an AJAX call to refresh data
            });
        }
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            updateTransactionTimes();
        }, 30000);
    }
    
    // Update transaction times to show real-time feel
    function updateTransactionTimes() {
        const timeElements = document.querySelectorAll('.transaction-time');
        timeElements.forEach((element, index) => {
            const currentTime = element.textContent;
            if (currentTime.includes('minutes ago')) {
                const minutes = parseInt(currentTime.match(/\d+/)[0]);
                element.textContent = `${minutes + 1} minutes ago`;
            } else if (currentTime.includes('hour ago')) {
                element.textContent = '1 hour ago';
            } else if (currentTime.includes('hours ago')) {
                const hours = parseInt(currentTime.match(/\d+/)[0]);
                element.textContent = `${hours} hours ago`;
            }
        });
    }
    
    // Initialize anomaly detection features
    function initAnomalyUpdates() {
        const anomalyBtn = document.querySelectorAll('.transaction-box')[1].querySelector('.action-btn');
        if (anomalyBtn) {
            anomalyBtn.addEventListener('click', function() {
                showNotification('Anomaly detection settings updated', 'info');
            });
        }
    }
    
    // Notification system (reused from dashboard)
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
});
