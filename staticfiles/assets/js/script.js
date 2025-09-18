document.addEventListener('DOMContentLoaded', () => {
    // --- THEME MANAGEMENT ---
    const themeCheckbox = document.getElementById('theme-checkbox');
    const applyTheme = (theme) => {
        document.body.classList.toggle('dark-mode', theme === 'dark-mode');
        if (themeCheckbox) themeCheckbox.checked = (theme === 'dark-mode');
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
            localStorage.setItem('theme', newTheme);
            applyTheme(newTheme);
        });
    }

    // --- DASHBOARD PAGE LOGIC ---
    if (document.body.classList.contains('dashboard-page')) {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const logoutBtn = document.getElementById('logout-btn');
        const profileBtn = document.getElementById('profile-btn');
        const profileDropdown = document.getElementById('profile-dropdown');
        
        // Sidebar toggle functionality
        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
                document.body.classList.toggle('sidebar-collapsed');
            });
        }
        
        // Profile dropdown functionality
        if (profileBtn && profileDropdown) {
            profileBtn.addEventListener('click', () => {
                profileDropdown.classList.toggle('show');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
                    profileDropdown.classList.remove('show');
                }
            });
        }
        
        // Logout functionality
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                // Redirect to logout URL
                window.location.href = '/logout/';
            });
        }
    }
    
    // --- CEO DASHBOARD SPECIFIC LOGIC ---
    if (document.body.classList.contains('ceo-dashboard-page')) {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const logoutBtn = document.getElementById('logout-btn');
        const profileBtn = document.getElementById('profile-btn');
        const profileDropdown = document.getElementById('profile-dropdown');
        
        // Sidebar toggle functionality
        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
                document.body.classList.toggle('sidebar-collapsed');
            });
        }
        
        // Profile dropdown functionality
        if (profileBtn && profileDropdown) {
            profileBtn.addEventListener('click', () => {
                profileDropdown.classList.toggle('show');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
                    profileDropdown.classList.remove('show');
                }
            });
        }
        
        // Logout functionality
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                // Redirect to logout URL
                window.location.href = '/logout/';
            });
        }
    }
});