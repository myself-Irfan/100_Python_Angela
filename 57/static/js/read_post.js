document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('post-content');
    const postId = container.dataset.postId;

    fetch(`/api/get?id=${postId}`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    })
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
        container.innerHTML = `
            <h2 class="card-title">${post.title}</h2>
            <h5 class="card-subtitle mb-2 text-muted">${post.subtitle || 'No content available'}</h5>
            <p class="card-text mt-4">${post.body || 'No content available'}</p>
            <p class="card-text">${post.author}</p>
            <p class="card-text">${post.create_date}</p>
            <a href="/edit_post/${post.id}" class="btn btn-warning">Edit Post</a>
            <button class="btn btn-danger" id="delete-post-btn">Delete Post</button>
        `;

            const deleteBtn = document.getElementById('delete-post-btn');
            deleteBtn.addEventListener('click', () => {
                if (confirm('Are you sure you want to delete this post?')){
                    fetch(`/api/delete/${postId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        }
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.message) {
                            alert('Post deleted successfully');
                            window.location.href = '/';
                        } else {
                            alert('Failed to delete post');
                        }
                    })
                    .catch(err => {
                        alert('An error occurred while attempting to delete the post');
                    });
                }
            });
    })
    .catch(err => {
        console.log('Failed to fetch post');

        const { message, statusCode } = err;

        let alertClass = 'alert-danger';

        if (statusCode === 404) {
            alertClass = 'alert-warning';
        }

        container.innerHTML = `
            <div class="col">
                <div class="alert ${alertClass} w-100" role="alert">
                    ${message || 'An error occurred while loading post. Please try again later.'}
                </div>
            </div>
        `;
    });
});