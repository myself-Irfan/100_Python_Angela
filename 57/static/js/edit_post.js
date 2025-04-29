document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('edit-post-form');
    const postId = form?.dataset.postId;
    const submitBtn = form?.querySelector('button[type="submit"]');
    const alertPlaceholder = document.getElementById('alert-placeholder');

    if (!form || !postId || !submitBtn) {
        console.error('Form, postId or submit button not found');
        renderAlert(alertPlaceholder, 'Unable to load edit form', 'danger');
        return;
    }

    const ogTxt = submitBtn.textContent;

    getPost(postId)
    .then(post => {
        document.getElementById('title').value = post.title || '';
        document.getElementById('subtitle').value = post.subtitle || '';
        document.getElementById('body').value = post.body || '';

        form.addEventListener('submit', async event => {
            event.preventDefault();
            submitBtn.disabled = true;
            submitBtn.textContent = 'Updating...';

            const updatedPost = {
                title: document.getElementById('title').value.trim(),
                subtitle: document.getElementById('subtitle').value.trim() || undefined,
                body: document.getElementById('body').value.trim() || undefined
            };

            if (!updatedPost.title || !updatedPost.body) {
                renderAlert(alertPlaceholder, 'Title and Body are required', 'warning');
                submitBtn.disabled = false;
                submitBtn.textContent = ogTxt;
                return;
            }

            try {
                await updatePost(postId, updatedPost);
                alert('Post updated successfully');
                window.location.href = `/read_post/${postId}`;
            } catch (err) {
                console.error('Update error: ', err);
                renderAlert(
                    alertPlaceholder,
                    err.messages || 'An error occurred while updating the post',
                    'danger'
                )
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = ogTxt;
            }
        });
    })
    .catch(err => {
        console.error('Fetch error: ', err);
        renderAlert(
            alertPlaceholder,
            err.messages || 'An error occurred while loading updated post',
            err.message.includes('No post') ? 'warning' : 'danger'
        );
    });
});