"""
Flask web application for Library Management System.

This app provides a web interface to manage books in a library,
including adding, borrowing, and returning books.
"""

from flask import Flask, request, render_template, redirect, url_for, flash
from functions import Book, Library
from dotenv import load_dotenv
import os

load_dotenv()   #Load the.env file

# Create Flask app instance
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')  # Required for flash messages

# Initialize global library instance
lib = Library()

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for the library homepage.

    Handles GET requests to display available books and POST requests
    to add, borrow, or return books.
    """
    if request.method == "POST":
        # Get form data
        action = request.form.get('action')
        title = request.form.get('title').lower()  # Convert to lowercase for consistency
        author = request.form.get('author').lower()

        if action == 'add':
            # Create and add new book
            book = Book(title, author)
            message = lib.add_book(book)
            flash(message, 'success' if 'successfully' in message else 'danger')
        elif action == 'borrow':
            # Borrow existing book
            book = Book(title, author)
            message = lib.borrow_book(book)
            flash(message, 'success' if 'successfully' in message else 'danger')
        elif action == 'return':
            # Return borrowed book
            book = Book(title, author)
            message = lib.return_book(book)
            flash(message, 'success' if 'successfully' in message else 'danger')

        # Redirect to avoid form resubmission
        return redirect(url_for('index'))

    # Get available books for display
    available_books = lib.get_available_books()
    return render_template('index.html', books=available_books)

if __name__ == "__main__":
    # Run the Flask app in debug mode(ONLY IN DEVELOPMENT ENVIRONMENT)
    app.run(debug=True)