document.addEventListener('DOMContentLoaded', () => {
    const postsContainer = document.getElementById('posts-container');
    const alertContainer = document.getElementById('alert-placeholder')

    if (!postsContainer || !alertContainer) {
        console.error('Posts/alert container not found');
        return;
    }

    async function loadPosts() {
        showLoading(postsContainer);
        try {
            const result = await getPosts();
            clearLoading(postsContainer);

            const posts = Array.isArray(result.data) ? result.data : [];
            if (!posts.length)  {
                renderAlert(alertContainer, 'No posts found', 'warning')
                return;
            }
            result.data.forEach(post => renderPostCard(post, postsContainer));
        } catch (error) {
            console.error(`Error loading posts: ${error}`);
            clearLoading(postsContainer);
            renderAlert(
                alertContainer,
                error.message || 'Failed to load posts',
                message.includes('not found') ? 'warning' : 'danger'
            );
        }
    }

    loadPosts();

});