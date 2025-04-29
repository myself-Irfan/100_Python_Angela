document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('posts-container');
    if (!container) {
        console.error('Posts container not found');
        return;
    }

    showLoading(container);

    getPosts()
    .then(posts => {
        clearLoading(container);
        if (!posts || posts.length === 0) {
            renderAlert(container, 'No posts found', 'warning');
            return;
        }
        posts.forEach(post => renderPostCard(post, container));
    })
    .catch(err => {
        console.error('Failed to fetch posts: ', err);
        clearLoading(container);
        renderAlert(
            container,
            err.message || 'An error occurred while loading posts',
            err.message.includes('No posts') ? 'warning' : 'danger'
        );
    });
});