// Transaction Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize real-time updates
    initRealTimeUpdates();
    
    // Initialize theme switching
    initThemeSwitch();
    
    // Initialize sidebar toggle
    initSidebarToggle();
    
    // Initialize profile dropdown
    initProfileDropdown();
    
    // Initialize logout functionality
    initLogout();
});

function initRealTimeUpdates() {
    // Update data every 5 seconds
    setInterval(updateTransactionData, 5000);
    
    // Initial update
    updateTransactionData();
}

function updateTransactionData() {
    fetch('/api/transactions/')
        .then(response => response.json())
        .then(data => {
            updateTransactionList(data.transactions);
            updateAnomalyList(data.alerts);
            updateAccountBalance(data.account_balance);
            updateStatistics(data);
        })
        .catch(error => {
            console.error('Error fetching transaction data:', error);
        });
}

function updateTransactionList(transactions) {
    const transactionList = document.getElementById('transaction-list');
    if (!transactionList) return;
    
    if (transactions.length === 0) {
        transactionList.innerHTML = `
            <div class="no-transactions">
                <i class="fas fa-info-circle"></i>
                <p>No transactions found. Start the transaction generator to see live data.</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    transactions.forEach(transaction => {
        const isCredit = transaction.receiver === 'TechCorp Solutions';
        const amountClass = isCredit ? 'credit' : 'debit';
        const iconClass = isCredit ? 'arrow-down' : 'arrow-up';
        const amountSign = isCredit ? '+' : '-';
        const description = isCredit ? 
            `Payment Received - ${transaction.sender}` : 
            `Payment Sent - ${transaction.receiver}`;
        
        const anomalyBadge = transaction.is_anomaly ? 
            '<span class="anomaly-badge">ANOMALY</span>' : '';
        
        html += `
            <div class="transaction-item ${transaction.is_anomaly ? 'anomaly' : ''}">
                <div class="transaction-icon ${amountClass}">
                    <i class="fas fa-${iconClass}"></i>
                </div>
                <div class="transaction-details">
                    <div class="transaction-description">
                        ${description}
                        ${anomalyBadge}
                    </div>
                    <div class="transaction-time">${transaction.time_ago}</div>
                </div>
                <div class="transaction-amount ${amountClass}">
                    ${amountSign}₹${parseFloat(transaction.amount).toLocaleString('en-IN', {minimumFractionDigits: 2})}
                </div>
            </div>
        `;
    });
    
    transactionList.innerHTML = html;
}

function updateAnomalyList(alerts) {
    const anomalyList = document.getElementById('anomaly-list');
    if (!anomalyList) return;
    
    if (alerts.length === 0) {
        anomalyList.innerHTML = `
            <div class="no-alerts">
                <i class="fas fa-shield-alt"></i>
                <p>No active alerts. All transactions are normal.</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    alerts.forEach(alert => {
        const iconClass = alert.severity === 'HIGH' ? 'exclamation-triangle' : 
                         alert.severity === 'MEDIUM' ? 'exclamation-circle' : 'info-circle';
        
        html += `
            <div class="anomaly-item ${alert.severity.toLowerCase()}">
                <div class="anomaly-icon">
                    <i class="fas fa-${iconClass}"></i>
                </div>
                <div class="anomaly-details">
                    <div class="anomaly-title">${alert.title}</div>
                    <div class="anomaly-description">${alert.description}</div>
                    <div class="anomaly-time">${alert.time_ago}</div>
                </div>
                <div class="anomaly-severity ${alert.severity.toLowerCase()}">${alert.severity}</div>
            </div>
        `;
    });
    
    anomalyList.innerHTML = html;
}

function updateAccountBalance(balance) {
    const balanceElement = document.querySelector('.balance-amount');
    if (balanceElement) {
        balanceElement.textContent = `₹${parseFloat(balance).toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
    }
}

function updateStatistics(data) {
    // Update transaction stats
    const totalElement = document.querySelector('.transaction-stats .stat-item:nth-child(1) .stat-value');
    const anomaliesElement = document.querySelector('.transaction-stats .stat-item:nth-child(2) .stat-value');
    const percentageElement = document.querySelector('.transaction-stats .stat-item:nth-child(3) .stat-value');
    
    if (totalElement) totalElement.textContent = data.total_transactions;
    if (anomaliesElement) anomaliesElement.textContent = data.anomaly_count;
    if (percentageElement) {
        const percentage = data.total_transactions > 0 ? 
            ((data.anomaly_count / data.total_transactions) * 100).toFixed(1) : '0.0';
        percentageElement.textContent = percentage + '%';
    }
}

function initThemeSwitch() {
    const themeCheckbox = document.getElementById('theme-checkbox');
    if (!themeCheckbox) return;
    
    // Load saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        themeCheckbox.checked = true;
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
    }
    
    themeCheckbox.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.remove('dark-mode');
            document.body.classList.add('light-mode');
            localStorage.setItem('theme', 'light');
        } else {
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        }
    });
}

function initSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (!sidebarToggle || !sidebar) return;
    
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        
        const icon = this.querySelector('i');
        const text = this.querySelector('span');
        
        if (sidebar.classList.contains('collapsed')) {
            icon.className = 'fas fa-chevron-right';
            text.textContent = 'Expand';
        } else {
            icon.className = 'fas fa-chevron-left';
            text.textContent = 'Collapse';
        }
    });
}

function initProfileDropdown() {
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');
    
    if (!profileBtn || !profileDropdown) return;
    
    profileBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        profileDropdown.classList.toggle('show');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
        profileDropdown.classList.remove('show');
    });
}

function initLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (!logoutBtn) return;
    
    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Show confirmation dialog
        if (confirm('Are you sure you want to log out?')) {
            window.location.href = '/logout/';
        }
    });
}

// Live time update
function updateLiveTime() {
    const liveTimeElement = document.getElementById('live-time');
    if (liveTimeElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        liveTimeElement.textContent = ` • ${timeString}`;
    }
}

// Update time every second
setInterval(updateLiveTime, 1000);
updateLiveTime(); // Initial call
