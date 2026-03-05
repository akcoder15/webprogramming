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