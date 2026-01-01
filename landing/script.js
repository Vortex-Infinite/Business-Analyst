// ===== DOM Elements =====
const navbar = document.querySelector('.navbar');
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
const tabBtns = document.querySelectorAll('.tab-btn');

// ===== Initialize on DOM Load =====
document.addEventListener('DOMContentLoaded', () => {
    initScrollAnimations();
    initCounters();
    initAnalyticsChart();
});

// ===== Navbar Scroll Effect =====
let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    lastScrollY = window.scrollY;
});

// ===== Mobile Nav Toggle =====
navToggle?.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
});

// Close mobile menu on link click
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
    });
});

// ===== Scroll Animations (Fade In) =====
function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    // Observe elements
    const animateElements = document.querySelectorAll(
        '.feature-card, .security-card, .testimonial-card, .metric-card'
    );

    animateElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = `opacity 0.5s ease ${index * 0.1}s, transform 0.5s ease ${index * 0.1}s`; // Staggered
        observer.observe(el);
    });

    // Add animation class styles dynamically
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
}

// ===== Counter Animation =====
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseFloat(counter.dataset.count);
                const duration = 1500; // Faster
                const step = target / (duration / 16);
                let current = 0;

                const updateCounter = () => {
                    current += step;
                    if (current < target) {
                        counter.textContent = current.toFixed(target % 1 === 0 ? 0 : 1);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target.toString();
                    }
                };

                updateCounter();
                observer.unobserve(counter);
            }
        });
    }, observerOptions);

    counters.forEach(counter => observer.observe(counter));
}

// ===== Tab Buttons (Chart) =====
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        updateChart(btn.dataset.tab);
    });
});

// ===== Analytics Chart (Chart.js) =====
let analyticsChart = null;

function initAnalyticsChart() {
    const ctx = document.getElementById('analyticsChart');
    if (!ctx) return;

    // Professional colors
    const colorprimary = '#2563eb'; // Royal Blue
    const colorSecondary = '#64748b'; // Slate

    const chartData = {
        revenue: {
            current: [45, 52, 48, 61, 55, 67, 62, 75, 70, 82, 78, 95],
            previous: [38, 42, 40, 52, 48, 58, 55, 62, 58, 68, 65, 78]
        },
        profit: {
            current: [22, 28, 24, 32, 29, 36, 33, 42, 38, 48, 44, 55],
            previous: [18, 22, 19, 26, 24, 30, 28, 34, 31, 38, 35, 42]
        },
        expenses: {
            current: [23, 24, 24, 29, 26, 31, 29, 33, 32, 34, 34, 40],
            previous: [20, 20, 21, 26, 24, 28, 27, 28, 27, 30, 30, 36]
        }
    };

    const labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'];

    analyticsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Current Year',
                    data: chartData.revenue.current,
                    borderColor: colorprimary,
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0, // Clean look
                    pointHoverRadius: 4,
                    borderWidth: 2
                },
                {
                    label: 'Previous Year',
                    data: chartData.revenue.previous,
                    borderColor: colorSecondary,
                    backgroundColor: 'transparent',
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 4,
                    borderWidth: 2,
                    borderDash: [5, 5] // Dashed for previous year
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)', // Slate 900
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    padding: 10,
                    cornerRadius: 4,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            return context.dataset.label + ': ' + context.parsed.y + 'M';
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#64748b',
                        font: { size: 10, family: "'Inter', sans-serif" }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        borderDash: [5, 5]
                    },
                    ticks: {
                        color: '#64748b',
                        font: { size: 10, family: "'Inter', sans-serif" },
                        callback: function (value) { return value + 'M'; }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });

    // Store data
    analyticsChart.chartData = chartData;
}

function updateChart(type) {
    if (!analyticsChart || !analyticsChart.chartData) return;

    const data = analyticsChart.chartData[type];
    if (!data) return;

    analyticsChart.data.datasets[0].data = data.current;
    analyticsChart.data.datasets[1].data = data.previous;
    analyticsChart.update();
}

// ===== Smooth Scroll =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ===== Mockup Animation =====
window.addEventListener('load', () => {
    const bars = document.querySelectorAll('.chart-bars .bar');
    bars.forEach((bar, index) => {
        bar.style.transform = 'scaleY(0)';
        bar.style.transformOrigin = 'bottom';
        bar.style.transition = `transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) ${index * 0.1}s`; // Bouncy effect

        setTimeout(() => {
            bar.style.transform = 'scaleY(1)';
        }, 300);
    });
});

console.log('ORBIS AI Landing Page - Professional Edition');
