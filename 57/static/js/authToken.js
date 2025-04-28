function getAccessToken() {
    return localStorage.getItem('access_token');
}

async function fetchWithAuth(url, options = {}) {
    if (!options.headers) options.headers = {};
    options.headers['Authorization'] = 'Bearer ' + getAccessToken();

    let response = await fetch(url, options);

    if (response.status === 401){
        const refreshed = await refreshToken();
        if (refreshed) {
            options.headers['Authorization'] = 'Bearer ' + getAccessToken();
            response = await fetch(url, options);
        } else {
            window.location.href = '/login';
        }
    }

    return response;
}

async function refreshToken() {
    try {
        const res = await fetch('/refresh', {
            method: 'POST',
            credentials: 'include'
        });
        if !(res.ok) return false;

        const data = await res.json();
        localStorage.setItem('access_token', data.access_token);
        return true
    } catch {
        return false;
    }
}