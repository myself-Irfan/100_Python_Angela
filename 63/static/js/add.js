function addBook() {
    const title = document.querySelector('#book-name').value
    const author = document.querySelector('#book-author').value
    const rating = document.querySelector('#book-rating').value

    if (!title || !author || !rating) {
        alert('Please fill in all the fields');
        return;
    }

    const data = {
        title,
        author,
        rating
    };

    fetch('/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            alert('Book added successfully');
            window.location.href = '/';
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data) {
            alert(data.error || 'Error adding book');
        }
    })
    .catch(error => {
        console.error('Error:', error)
        alert('Failed to add book')
    });
}