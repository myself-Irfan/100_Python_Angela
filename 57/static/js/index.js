document.addEventListener('DOMContentLoaded', ()=> {
    const container = document.getElementById('posts-container')

    fetch('/api/get')
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
    .then(data => {
        if (Array.isArray(data)) {
            if (data.length === 0) {
                container.innerHTML = `
                    <div class="col">
                        <div class="alert alert-warning w-100" role="alert">
                            No posts found
                        </div>
                    </div>
                `;
                return;
            }

            data.forEach(post => {
                const postCard = `
                    <div class="col">
                        <div class="card h-100 shadow-sm border-0">
                            <img src="https://placehold.co/300x150" class="card-img-top" alt="Placeholder image">
                            <div class="card-body d-flex flex-column">
                                <h5 class="card-title">${post.title}</h5>
                                <h6 class="card-subtitle text-muted mb-3">${post.subtitle}</h6>
                                <div class="mt-auto">
                                    <a href="/post/${post.id}" class="btn btn-primary">Read</a>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', postCard)
            });
        } else {
            throw new Error('Invalid response format')
        }
    })
    .catch(err => {
        console.log('Failed to fetch posts');

        const { message, statusCode } = err;

        let alertClass = 'alert-danger';

        if (statusCode === 404) {
            alertClass = 'alert-warning';
        }

        container.innerHTML = `
            <div class="col">
                <div class="alert ${alertClass} w-100" role="alert">
                    ${message || 'An error occurred while loading posts. Please try again later.'}
                </div>
            </div>
        `;
    });
});