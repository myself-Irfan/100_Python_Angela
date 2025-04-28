document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = form.querySelector('button[type="submit"]')

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const email = formData.get('email');
        const password = formData.get('password');

        submitBtn.disabled = true
        const ogTxt = submitBtn.textContent;
        submitBtn.textContent = 'Logging in...'

        try {
            const response = await fetch('/user/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password }),
                credentials: 'include'
            });

            if (response.ok)  {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);

                window.location.href = '/';
            } else {
                const errorData = await response.json();
                alert(errorData.message || 'Login Failed');

                submitBtn.disabled = false;
                submitBtn.textContent = ogTxt;
            }
        } catch (error) {
            console.error('Login error: ', error);
            alert('An unexpected error occurred. Please try again later.')

            submitBtn.disabled = false;
            submitBtn.textContent = ogTxt;
        }

    });
});