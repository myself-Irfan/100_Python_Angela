document.addEventListener('DOMContentLoaded', () => {
    fetch('api/get')
    .then(response => response.json())
    .then(books => {
        const tableBody = document.querySelector('#books-table tbody');

        if (books.length === 0) {
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = `
                <td colspan='5' class='text-center'>Library is empty. Add some books</td>
            `;
            tableBody.appendChild(emptyRow);
        } else {
            books.forEach((book, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.rating}</td>
                <td>
                    <button class='btn btn-danger' type='button' onClick='deleteBook(${book.id})'>Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error fetching books:', error);
        alert('Error getting books:', error);
    });
});

function deleteBook(bookId) {
    if (confirm('Are you sure you want to delete this book?')) {
        fetch(`/api/delete/${bookId}`,
            {method: 'DELETE'}
        )
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Failed to delete the book')
            }
        })
        .catch(error => console.error('Error:', error));
    }
}