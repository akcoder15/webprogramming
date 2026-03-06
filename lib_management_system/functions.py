import sqlite3

class Book:
    """
    Represents a book in the library system.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        is_available (bool): Availability status of the book.
    """
    def __init__(self, title, author):
        """
        Initializes a new Book instance.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
        """
        self.title = title
        self.author = author
        self.is_available = True


class Library:
    """
    Manages the library's book collection using SQLite database.

    Attributes:
        conn (sqlite3.Connection): Database connection.
        cur (sqlite3.Cursor): Database cursor for executing queries.
    """
    def __init__(self, db_name="library.db"):
        """
        Initializes the Library with a SQLite database.

        Args:
            db_name (str): Name of the database file. Defaults to "library.db".
        """
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Creates the books table in the database if it doesn't exist.
        The table includes id, title, author, and is_available columns.
        """
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

    def add_book(self, book):
        """
        Adds a new book to the library database.

        Args:
            book (Book): The book object to add.

        Returns:
            str: Success or error message.
        """
        try:
            self.cur.execute("INSERT INTO books(title, author, is_available) VALUES (?,?,?)",
                            (book.title, book.author, 1 if book.is_available else 0))
            self.conn.commit()
            return f"Book '{book.title}' by {book.author} added successfully."
        except sqlite3.IntegrityError:
            return f"Book '{book.title}' by {book.author} is already in the library."

    def borrow_book(self, book):
        """
        Marks a book as borrowed if it's available.

        Args:
            book (Book): The book to borrow.

        Returns:
            str: Success or error message.
        """
        self.cur.execute("""
            UPDATE books 
            SET is_available = 0 
            WHERE title=? AND author=? AND is_available = 1
        """, (book.title, book.author))
        
        if self.cur.rowcount > 0:
            self.conn.commit()
            book.is_available = False
            return f"You have successfully borrowed '{book.title}' by {book.author}."
        else:
            return f"'{book.title}' by {book.author} is not available or does not exist."

    def return_book(self, book):
        """
        Marks a book as returned if it was borrowed.

        Args:
            book (Book): The book to return.

        Returns:
            str: Success or error message.
        """
        # First check if the book exists and is currently borrowed
        self.cur.execute("SELECT is_available FROM books WHERE title=? AND author=?", (book.title, book.author))
        result = self.cur.fetchone()
        
        if result is None:
            return f"'{book.title}' by {book.author} does not exist in the library."
        elif result[0] == 1:
            return f"'{book.title}' by {book.author} is already available and was not borrowed."
        else:
            # Book exists and is borrowed, so return it
            self.cur.execute("""
                UPDATE books 
                SET is_available = 1 
                WHERE title=? AND author=? AND is_available = 0
            """, (book.title, book.author))
            
            if self.cur.rowcount > 0:
                self.conn.commit()
                book.is_available = True
                return f"'{book.title}' by {book.author} has been returned successfully."
            else:
                return f"Error: Unable to return '{book.title}' by {book.author}."

    def get_available_books(self):
        """
        Retrieves a list of all available books.

        Returns:
            list: List of tuples containing (title, author) for available books.
        """
        self.cur.execute("SELECT title, author FROM books WHERE is_available = 1")
        return self.cur.fetchall()

    def close(self):
        """
        Closes the database connection and cursor.
        """
        self.cur.close()
        self.conn.close()
