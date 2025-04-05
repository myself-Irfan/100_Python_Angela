document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('edit-post-form');
    const postId = form ? form.dataset.postId : null;

    if (!postId) {
        alert('Post ID not found.');
        return;
    }

    fetch(`/api/get?id=${postId}`)
    .then(res => {
        if (!res.ok) {
            return res.json().then(data => {
                const message = data.message || data.error || 'Unknown error';
                const statusCode = res.status;

                throw { message, statusCode };
            });
        }
        return res.json();
    })
    .then(post => {
        document.getElementById('title').value = post.title;
        document.getElementById('subtitle').value = post.subtitle || '';
        document.getElementById('body').value = post.body || '';

        form.addEventListener('submit', (event) => {
            event.preventDefault();

            const updatedPost = {
                title: document.getElementById('title').value,
                subtitle: document.getElementById('subtitle').value,
                body: document.getElementById('body').value
            };

            fetch(`/api/update/${post.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedPost)
            })
            .then(res => res.json())
            .then(data => {
                if (data.message) {
                    alert('Post updated successfully');
                    window.location.href = `/read_post/${post.id}`;
                } else {
                    alert('Failed to update post. Please try again later!');
                }
            })
            .catch(err => {
                alert('An error occurred while attempting to update the post. Please try again later');
            });
        });
    })
    .catch(err => {
        alert('An error occurred while fetching post data.');
        console.error(err);
    });
});
