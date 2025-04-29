async function getPosts() {
    const response = await fetchWithAuth('/api/get');
    if (!response) throw new Error('Redirected to login');
    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message|| 'Failed to fetch posts');
    }
    return response.json();
}

async function getPost(id) {
    const response = await fetchWithAuth(`/api/get?id=${id}`);
    if (!response) throw new Error('Redirected to login');
    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Failed to fetch post');
    }
    return response.json();
}

async function createPost(data) {
    const response = await fetchWithAuth('/api/post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    if (!response) throw new Error('Redirected to login');
    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Failed to create post')
    }
    return response.json();
}

async function updatePost(id, data) {
    const response = await fetchWithAuth(`/api/update/${id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    if (!response) throw new Error('Redirected to login');
    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Failed to update post');
    }
    return response.json();
}

async function deletePost(id) {
    const response = await fetchWithAuth(`/api/delete/${id}`, {
        method: 'DELETE'
    });
    if (!response) throw new Error('Redirected to login')
    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Failed to delete post');
    }
    throw response.json();
}