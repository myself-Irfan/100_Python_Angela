document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = form.querySelector('button[type="submit"]')
    const ogTxt = submitBtn.textContent;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const email = formData.get('email');
        const password = formData.get('password');

        submitBtn.disabled = true
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

            const data = await response.json();

            if (response.ok && data.data && data.data.access_token)  {
                localStorage.setItem('access_token', data.data.access_token);
                window.location.href = '/';
            } else {
                alert(data.message || 'Login Failed');
                resetBtn();
            }
        } catch (error) {
            console.error('Login error: ', error);
            alert('An unexpected error occurred. Please try again later.')

            resetBtn();
        }

    });

    function resetBtn() {
        submitBtn.disabled = false;
        submitBtn.textContent = ogTxt;
    }

});