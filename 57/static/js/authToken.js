// return locally stored access_token

function getAccessToken() {
    return localStorage.getItem('access_token');
}

async function fetchWithAuth(url, options = {}) {
    if (!options.headers) options.headers = {};
    options.headers['Authorization'] = `Bearer ${getAccessToken()}`;

    try {
        let response = await fetch(url, options);

        if (response.status === 401){
            const refreshed = await refreshToken();
            if (refreshed) {
                options.headers['Authorization'] = `Bearer ${getAccessToken()}`;
                response = await fetch(url, options);
            } else {
                window.location.href = 'user/login';
                return null;
            }
        }

        return response;
    } catch (error) {
        console.error(`Fetch error for ${url}: ${error}`);
        throw new Error('Network error occurred');
    }
}

async function refreshToken() {
    try {
        const res = await fetch('/user/api/refresh-token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`
            }
        });

        if (!res.ok) {
            console.error(`Token refresh failed: ${res.status}`);
            return false;
        }

        const data = await res.json();
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        return true
    } catch (error) {
        console.error(`Error refreshing token: ${error}`);
        return false;
    }
}