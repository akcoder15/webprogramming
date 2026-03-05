# Library Management System Classes
# This module defines the Book and Library classes for managing a book collection using SQLite.

import sqlite3

# Book class represents a single book with title, author, and availability status
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True  # Books start as available

# Library class handles database operations for book management
class Library:
    def __init__(self, db_name="library.db"):
        # Connect to SQLite database with thread safety for Flask
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()  # Initialize database table
    
    # Create the books table if it doesn't exist
    def create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                is_available INTEGER,
                UNIQUE(title,author)
            )
        ''')
        self.conn.commit()

   # Add a new book to the library
    def add_book(self, book):
        try:
            self.cur.execute("INSERT INTO books(title, author, is_available) VALUES (?,?,?)",
                            (book.title, book.author, 1 if book.is_available else 0))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"{book.title} by {book.author} is already added")
    
    # Borrow a book (mark as unavailable)
    def borrow_book(self, book):
        self.cur.execute("""
            UPDATE books 
            SET is_available = 0 
            WHERE title=? AND author=? AND is_available = 1
        """, (book.title, book.author))
        
        if self.cur.rowcount > 0:
            self.conn.commit()
            book.is_available = 0
            print(f"Success: You borrowed {book.title} by {book.author}.")
        else:
            print(f"Error: {book.title} by {book.author} is already borrowed or doesn't exist.")