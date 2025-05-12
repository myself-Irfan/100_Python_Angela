document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('edit-post-form');
    const postId = form?.dataset.postId;
    const alertPlaceholder = document.getElementById('alert-placeholder');

    if (!form || !postId || !alertPlaceholder) {
    console.error('HTML element missing');
    renderAlert(alertPlaceholder, 'Unable to load edit form', 'danger');
    return;
}

    async function loadPost() {
        showLoading(form);
        try {
            const result = await getPost(postId);
            clearLoading(form);
            const post = result.data;
            renderEditPostForm(post, form);
        } catch (error) {
            console.error(`Failed to load post: ${error}`);
            clearLoading(form);
            const message = error.message || 'An error occurred while loading the post';
            const type = message.includes('not found') ? 'warning' : 'danger';
            renderAlert(alertPlaceholder, message, type);
        }
    }

    form.addEventListener('submit', async event => {
        const submitBtn = form?.querySelector('button[type="submit"]');

        const ogTxt = submitBtn.textContent;

        event.preventDefault();
        submitBtn.disabled = true;
        submitBtn.textContent = 'Updating...';
        alertPlaceholder.innerHTML = '';

        const formData = new FormData(form);
        const data = {
            title: formData.get('title').trim(),
            subtitle: formData.get('subtitle')?.trim() || null,
            body: formData.get('body').trim()
        };

        if (!data.title || !data.body) {
            renderAlert(alertPlaceholder, 'Please fill in the all the required fields', 'warning');
            submitBtn.disabled  = false
            submitBtn.textContent = ogTxt;
            return;
        }

        if (data.title.length < 3) {
            renderAlert(alertPlaceholder, 'Title must be at least 3 characters long', 'warning');
            submitBtn.disabled = false;
            submitBtn.textContent = ogTxt;
            return;
        }

        try{
            const result =  await updatePost(postId, data);
            renderAlert(alertPlaceholder, result.message, 'success');
            setTimeout(() => {
                window.location.href = `/read_post/${postId}`;
            }, 1000);
        } catch (error) {
            console.error(`Failed to updatePost: ${error}`);
            const message = error.message || 'An error occurred while updating the post';
            const type = message.includes('not found') || message.includes('authorized') ? 'warning' : 'danger';
            renderAlert(alertPlaceholder, message, type);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = ogTxt;
        }
    })

    loadPost();

});