async function getPosts() {
    const response = await fetchWithAuth('/api/get');
    if (!response) throw new Error('Authentication required');

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message|| 'Failed to fetch posts');
    }
    return data;
}

async function getPost(id) {
    const response = await fetchWithAuth(`/api/get?id=${id}`);
    if (!response) throw new Error('Authentication required');

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || 'Failed to fetch post');
    }
    return data;
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

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || 'Failed to create post')
    }
    return result;
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

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || 'Failed to update post');
    }
    return result;
}

async function deletePost(id) {
    const response = await fetchWithAuth(`/api/delete/${id}`, {
        method: 'DELETE'
    });
    if (!response) throw new Error('Redirected to login')

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || 'Failed to delete post');
    }
    return data;
}