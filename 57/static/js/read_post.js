document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('post-content');
    const postId = container?.dataset.postId;
    const alertContainer = document.getElementById('alert-placeholder');

    if (!container || !postId || !alertContainer) {
        console.error('Post container/ID/alertContainer not found');
        renderAlert(container, 'Unable to load post due to internal error', 'danger');
        return;
    }

    async function loadPost() {
        showLoading(container);

        try {
            const result = await getPost(postId);
            clearLoading(container);
            renderPostContent(result.data, container);

            const deleteBtn = document.getElementById('delete-post-btn');
            if (!deleteBtn) {
                console.error(`Delete button not found for post: ${postId}`);
                renderAlert(alertContainer, 'Delete button not available', 'danger');
                return;
            }

            deleteBtn.addEventListener('click', async () => {
                if (!confirm('Confirm delete operation of selected post?')) return;

                deleteBtn.disabled = true;
                deleteBtn.textContent = 'Deleting...';

                try {
                    const data = await deletePost(postId);
                    renderAlert(alertContainer, data.message, 'success');
                    setTimeout(() => {
                        window.location.href = '/'
                    }, 1000);
                } catch (error) {
                    console.error('Error while deleting:', error);
                    renderAlert(
                        alertContainer,
                        error.message || 'An error occurred while deleting the post',
                        error.message.includes('not found') || error.message.includes('authorized') ? 'warning' : 'danger'
                    )
                    deleteBtn.disabled = false;
                    deleteBtn.textContent = 'Delete';
                }
            })

        } catch (error) {
            console.error(`Failed to fetch post: ${error}`)
            clearLoading(container);
            renderAlert(
                alertContainer,
                error.message || 'An error occurred while fetching the post',
                error.message.includes('not found') ? 'warning' : 'danger'
            )
        }
    }

    loadPost();
});