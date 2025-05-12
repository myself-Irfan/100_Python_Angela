document.addEventListener('DOMContentLoaded', () => {
    const loggedInLinks = document.getElementById('logged-in-links');
    const loggedOutLinks = document.getElementById('logged-out-links');
    const logoutLink = document.getElementById('logout-link');

    // Check if user is logged in by looking for access_token in localStorage
    const isLoggedIn = localStorage.getItem('access_token') !== null;

    // Toggle navbar links
    if (isLoggedIn) {
        loggedInLinks.style.display = 'flex';
        loggedOutLinks.style.display = 'none';
    } else {
        loggedInLinks.style.display = 'none';
        loggedOutLinks.style.display = 'flex';
    }

    // Handle logout
    logoutLink.addEventListener('click', (event) => {
        event.preventDefault();
        // Clear tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        // Redirect to login page
        window.location.href = '/user/login';
    });

    // Highlight active link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href === '/' && currentPath === '/index')) {
            link.classList.add('active');
        }
    });
});