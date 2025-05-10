document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const submitBtn = document.querySelector('button[type="submit"]');
    const alertPlaceholder = document.getElementById('alert-placeholder');

    if (!form || !submitBtn) {
        console.error('Form or submit button not found');
        if (alertPlaceholder) {
            renderAlert(alertPlaceholder, 'Unable to find register form', 'danger');
            return;
        }
    }

    const ogTxt = submitBtn.textContent;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            name: formData.get('name').trim(),
            email: formData.get('email').trim(),
            password: formData.get('password').trim()
        };

        if (!data.name || !data.email || !data.password) {
            renderAlert(alertPlaceholder, 'Please fill all the required fields', 'warning');
            return;
        }

        if (data.password.length < 6) {
            renderAlert(alertPlaceholder, 'Password must be at least 6 characters', 'warning');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Registering...';

        try {
            const response = await fetch('/user/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                alert('Registration successful! You can now login.');
                window.location.href = '/user/login';
            } else {
                renderAlert(
                    alertPlaceholder,
                    formatErrors(result.message) || 'Registration failed',
                    'warning'
                );
            }
        } catch (error) {
            console.error('Registration error: ', error);
            renderAlert(
                alertPlaceholder,
                error.message || 'Unexpected error',
                'danger'
            )
        } finally {
            resetBtn();
        }
    });

    function resetBtn() {
        submitBtn.disabled = false;
        submitBtn.textContent = ogTxt;
    }

    function formatErrors(errors) {
    if (typeof errors === 'string') return errors;

    let messages = [];
    for (const key in errors) {
        if (Array.isArray(errors[key])) {
            messages.push(`${key}: ${errors[key].join(', ')}`);
        } else {
            messages.push(`${key}: ${errors[key]}`);
        }
    }
    return messages.join('<br>');
    }

});