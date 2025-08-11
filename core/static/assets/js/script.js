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

    // --- EMPLOYEE LOGIN LOGIC ---
    const employeeLoginForm = document.getElementById('employee-login-form');
    if (employeeLoginForm) {
        employeeLoginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('employeeId').value;
            const password = document.getElementById('employeePassword').value;
            
            try {
                await mockSignIn(email, password, 'Employee');
                // Store user info in localStorage for dashboard access
                localStorage.setItem('currentUser', JSON.stringify({
                    email: email,
                    role: 'Employee'
                }));
                window.location.href = '/employee_home/';
            } catch (error) {
                alert(error.message);
            }
        });
    }

    // --- HR LOGIN LOGIC ---
    const hrLoginForm = document.getElementById('hr-login-form');
    const hrCredentialsForm = document.getElementById('hr-credentials-form');
    const hrOtpForm = document.getElementById('hr-otp-form');
    const otpVerifyForm = document.getElementById('otp-verify-form');
    
    if (hrLoginForm) {
        hrLoginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('hrId').value;
            const password = document.getElementById('hrPassword').value;
            
            try {
                await mockSignIn(email, password, 'HR');
                // Show OTP form
                hrCredentialsForm.classList.add('hidden');
                hrOtpForm.classList.remove('hidden');
            } catch (error) {
                alert(error.message);
            }
        });
    }
    
    if (otpVerifyForm) {
        otpVerifyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const otp = document.getElementById('otp').value;
            const email = document.getElementById('hrId').value;
            
            // Check if OTP matches the mock OTP
            if (otp === '123456') {
                // Store user info in localStorage for dashboard access
                localStorage.setItem('currentUser', JSON.stringify({
                    email: email,
                    role: 'HR'
                }));
                window.location.href = '/dashboard/';
            } else {
                alert('Invalid OTP. Please try again.');
            }
        });
    }
    
    // --- DASHBOARD PAGE LOGIC ---
    if (document.body.classList.contains('dashboard-page')) {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const logoutBtn = document.getElementById('logout-btn');
        const profileBtn = document.getElementById('profile-btn');
        const profileDropdown = document.getElementById('profile-dropdown');

        // Sidebar toggle
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
            });
        }
        
        // Logout
        if (logoutBtn) {
            logoutBtn.addEventListener('click', async () => {
                // Call Django logout endpoint
                await fetch('/logout/', { method: 'POST', credentials: 'same-origin', headers: { 'X-CSRFToken': getCSRFToken() } });
                localStorage.removeItem('currentUser');
                window.location.href = '/auth/employee_login/';
            });
        }

        // Profile Dropdown
        if (profileBtn) {
            profileBtn.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevents the window click event from firing immediately
                profileDropdown.classList.toggle('active');
            });
        }

        // Close dropdown when clicking outside
        window.addEventListener('click', () => {
            if (profileDropdown && profileDropdown.classList.contains('active')) {
                profileDropdown.classList.remove('active');
            }
        });

        // Live Clock
        const timeElement = document.getElementById('live-time');
        const updateClock = () => {
            if (timeElement) {
                const now = new Date();
                timeElement.textContent = now.toLocaleTimeString('en-US');
            }
        };
        setInterval(updateClock, 1000);
        updateClock(); // Initial call
    }
});

// Helper to get CSRF token from cookie
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return '';
}