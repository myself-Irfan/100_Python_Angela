document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('create-post-form');
    const submitBtn = form?.querySelector('button[type="submit"]');
    const alertPlaceholder = document.getElementById('alert-placeholder');

    if (!form || !submitBtn) {
        console.error('Form or submit button not found');
        renderAlert(alertPlaceholder, 'Unable to load post creation form', 'danger');
        return;
    }

    const ogTxt = submitBtn.textContent;

    form.addEventListener('submit', async event => {
        event.preventDefault();
        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating...';

        const formData = new FormData(form);
        const data = {
            title: formData.get('title').trim(),
            subtitle: formData.get('subtitle')?.trim() || null,
            body: formData.get('body').trim()
        };

        const subtitle = formData.get('subtitle')?.trim();
        if (subtitle) data.subtitle = subtitle;

        // client validation
        if (!data.title || !data.body) {
            renderAlert(
                alertPlaceholder,
                'Please fill in the required fields (title, body, subtitle)',
                'warning'
            );
            submitBtn.disabled = false;
            submitBtn.textContent = ogTxt;
            return;
        }

        if (data.title.length < 3) {
            renderAlert(
                alertPlaceholder,
                'Title must be at least 3 characters long',
                'warning'
            );
            submitBtn.disabled = false;
            submitBtn.textContent = ogTxt;
            return;
        }

        try {
            const result = await createPost(data);
            alert(result.message);
            form.reset();
            window.location.href = '/'
        } catch (error) {
            console.error('Create post error: ', error)
            renderAlert(
                alertPlaceholder,
                error.message || 'An error occurred while creating post',
                error.message.includes('not found') || error.message.includes('authorized') ? 'warning' : 'alert'
            )
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = ogTxt;
        }
    });
});