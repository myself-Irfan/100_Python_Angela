function deleteBook(bookId) {
    if (confirm('Are you sure you want to delete this book?')) {
        fetch(`api/delete/${bookId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Failed to delete the book. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the book.');
        });
    }
}
