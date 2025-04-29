document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('post-content');
    const postId = container?.dataset.postId;

    if (!container || !postId) {
        console.error('Post container or ID not found');
        renderAlert(container, 'Unable to load post', 'danger');
        return;
    }

    showLoading(container);

    getPost(postId)
    .then(post => {
        clearLoading(container)
        renderPostContent(post, container);

        const deleteBtn = document.getElementById('delete-post-btn');
        deleteBtn.addEventListener('click', async() => {
            if (!confirm('Confirm delete operation of selected post?')) return;

            deleteBtn.disabled = true;
            deleteBtn.textContent = 'Deleting...';

            try {
                await deletePost(postId);
                alert('Post deleted successfully');
                window.location.href = '/';
            } catch (err) {
                console.error('Deleting error: ', err);
                alert(err.message || 'An error occurred while deleting the post');
                deleteBtn.disabled = false;
                deleteBtn.textContent = 'Delete Post';
            }
        });
    })
    .catch (err => {
        console.error('Failed to fetch post: ', err)
        clearLoading(container);
            renderAlert(
            container,
            err.messages || 'An error occurred while deleting the post',
            err.message.include('No post') ? 'warning' : 'danger'
        )
    });
});