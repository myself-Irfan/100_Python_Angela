function renderPostCard(post, container) {
    const postCard = `
        <div class="col">
            <div class="card h-100 shadow-sm border-0">
                <img src="${post.image || 'https://placehold.co/300x150'}" class="card-img-top" alt="Post image">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${post.title}</h5>
                    <h6 class="card-subtitle text-muted mb-3">${post.subtitle || ''}</h6>
                    <div class="mt-auto">
                        <a href="/read_post/${post.id}" class="btn btn-primary">Read</a>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', postCard);
}

function renderPostContent(post, container) {
    container.innerHTML = `
        <h2 class="card-title">${post.title}</h2>
        <h5 class="card-subtitle mb-2 text-muted">${post.subtitle || 'No subtitle'}</h5>
        <p class="card-text mt-4">${post.body || 'No content available'}</p>
        <p class="card-text"><small class="text-muted">By ${post.author || 'Unknown'}</small></p>
        <p class="card-text"><small class="text-muted">${new Date(post.create_date || Date.now()).toLocaleDateString()}</small></p>
        <a href="/edit_post/${post.id}" class="btn btn-warning me-2">Edit Post</a>
        <button class="btn btn-danger" id="delete-post-btn">Delete Post</button>
    `;
}

function renderAlert(placeholder, message, type = 'danger') {
    if (!placeholder) return;
    placeholder.innerHTML = `
        <div class="alert alert-${type} alert-dismissible" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

function showLoading(container) {
    container.innerHTML = '<div class="spinner"></div>';
}

function clearLoading(container) {
    container.innerHTML = '';
}