import logging

from flask import Blueprint, request, jsonify, render_template
from model import Book, db

main = Blueprint('main', __name__)

# api

@main.route('/api/get', methods=['GET'])
def get_books():
    """
    get all books
    """
    try:
        all_books = Book.query.all()
        if not all_books:
            return jsonify({'message': 'No books found'}), 404
    except Exception as e:
        logging.error(f'Error while fetching books: {str(e)}')
        return jsonify({'error': 'Error occurred while fetching books'}), 500
    else:
        book_data = [
            {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'rating': book.rating
            }
            for book in all_books
        ]
        return jsonify(book_data), 200


@main.route('/api/add', methods=['POST'])
def create_book():
    """
    add a new book
    """
    try:
        data = request.json

        if not data:
            return jsonify({'error': 'No data provided'}), 400
    except Exception as e:
        logging.error(f'Error while posting: {str(e)}')
        return jsonify({'error': 'Error occurred while posting'}), 500
    else:
        title = data.get('title', 'N/A')
        author = data.get('author', 'N/A')
        rating = data.get('rating', 'N/A')

        new_book = Book(
            title=title,
            author=author,
            rating=rating
        )

    try:
        db.session.add(new_book)
        db.session.commit()
    except Exception as e:
        logging.error(f'Database error: {e}')
        return jsonify({'error': 'Error occurred while posting'}), 500

    return jsonify({'message': 'Book created'}), 201


@main.route('/api/delete/<int:book_id>', methods=['DELETE'])
def delete(book_id: int):
    try:
        book = Book.query.get(book_id)

        if not book:
            return jsonify({'error': f'No book found with id {book_id}'}), 404
    except Exception as e:
        logging.error(f'Error while deleting book with ID {book_id}: {str(e)}')
        return jsonify({'error': 'An error occurred while deleting the book'}), 500

    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        logging.error(f'Database error: {e}')
        return jsonify({'error': 'An error occurred while deleting the book'}), 500

    return jsonify({'message': 'Book deleted successfully'})

# render templates

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/add')
def add_book():
    return render_template('add.html')