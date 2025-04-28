document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const submitBtn = document.querySelector('button[type="submit"]');
    const ogTxt = submitBtn.textContent;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const name = formData.get('name');
        const email = formData.get('email');
        const password = formData.get('password');

        submitBtn.disabled = true;
        submitBtn.textContent = 'Registering...';

        try {
            const response = await fetch('/user/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, email, password }),
                credentials: 'include'
            });

            const data = await response.json();

            if (response.ok) {
                alert('Registration successful! You can now login.');
                window.location.href = '/login'
            } else {
                alert(data.message || 'Registration failed');
                resetBtn();
            }
        } catch (error) {
            console.error('Registration error: ', error);
            alert('An unexpected error occurred. Please try again.');

            resetBtn();
        }
    });

    function resetBtn() {
        submitBtn.disabled = false;
        submitBtn.textContent = ogTxt;
    }
});