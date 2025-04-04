document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('create-post-form');
    const alertPlaceholder = document.getElementById('alert-placeholder');

    function showAlert(message, type) {
        const alertElement = document.createElement('div');
        alertElement.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'alert', 'fade', 'show');
        alertElement.role = 'alert';
        alertElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        alertPlaceholder.appendChild(alertElement);
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            title: formData.get('title'),
            subtitle: formData.get('subtitle'),
            body: formData.get('body'),
            author: formData.get('author')
        };

        fetch('/api/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok){
                return response.json().then(err => {
                    throw new Error(err.error || 'Oops! Something went wrong')
                });
            }
            return response.json();
        })
        .then(data => {
            showAlert(data.message, 'success');
            form.reset();
        })
        .catch(error => {
            showAlert(error.message, 'danger');
        });
    });
});