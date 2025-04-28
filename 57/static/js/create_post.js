document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('create-post-form');
    const alertPlaceholder = document.getElementById('alert-placeholder');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            title: formData.get('title').trim(),
            body: formData.get('body').trim(),
            author: formData.get('author').trim()
        };

        const subtitle = formData.get('subtitle')?.trim();
        if (subtitle) {
            data.subtitle = subtitle;
        }

        fetch('/api/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
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
            alert(data.message);
            form.reset();
        })
        .catch(error => {
            alert(error.message);
        });
    });
});