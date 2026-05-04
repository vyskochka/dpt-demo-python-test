# Здесь должен быть менеджер базы данных согласно README.md

import sqlite3
from models.book import Book
from models.reader import Reader
from models.loan import Loan
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="library.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def close(self) -> None:
        self.conn.close()

    def create_tables(self) -> None:
        self.conn.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, isbn TEXT, year INTEGER, quantity INTEGER, available INTEGER)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS readers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone TEXT, registration_date TEXT)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER, reader_id INTEGER, loan_date TEXT, return_date TEXT, is_returned INTEGER DEFAULT 0)")
        self.conn.commit()

    def add_book(self, book: Book) -> int:
        c = self.conn.execute("INSERT INTO books (title, author, isbn, year, quantity, available) VALUES (?, ?, ?, ?, ?, ?)", (book.title, book.author, book.isbn, book.year, book.quantity, book.available))
        self.conn.commit()
        return c.lastrowid

    def get_book_by_id(self, book_id) -> Book | None:
        row = self.conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        if row:
            b = Book(row[1], row[2], row[3], row[4], row[5])
            b.id = row[0]
            b.available = row[6]
            return b
        return None

    def get_all_books(self) -> list[Book]:
        rows = self.conn.execute("SELECT * FROM books").fetchall()
        result = []
        for r in rows:
            b = Book(r[1], r[2], r[3], r[4], r[5])
            b.id = r[0]
            b.available = r[6]
            result.append(b)
        return result

    def update_book(self, book_id, **kwargs) -> bool:
        b = self.get_book_by_id(book_id)
        if not b:
            return False
        if "title" in kwargs: b.title = kwargs["title"]
        if "author" in kwargs: b.author = kwargs["author"]
        if "isbn" in kwargs: b.isbn = kwargs["isbn"]
        if "year" in kwargs: b.year = kwargs["year"]
        if "quantity" in kwargs: b.quantity = kwargs["quantity"]
        if "available" in kwargs: b.available = kwargs["available"]
        self.conn.execute("UPDATE books SET title=?, author=?, isbn=?, year=?, quantity=?, available=? WHERE id=?", (b.title, b.author, b.isbn, b.year, b.quantity, b.available, book_id))
        self.conn.commit()
        return True

    def delete_book(self, book_id) -> bool:
        c = self.conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()
        return c.rowcount > 0

    def search_books(self, query) -> list[Book]:
        rows = self.conn.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%")).fetchall()
        result = []
        for r in rows:
            b = Book(r[1], r[2], r[3], r[4], r[5])
            b.id = r[0]
            b.available = r[6]
            result.append(b)
        return result

    def add_reader(self, reader: Reader) -> int:
        c = self.conn.execute("INSERT INTO readers (name, email, phone, registration_date) VALUES (?, ?, ?, ?)", (reader.name, reader.email, reader.phone, reader.registration_date.isoformat()))
        self.conn.commit()
        return c.lastrowid

    def get_reader_by_id(self, reader_id) -> Reader | None:
        row = self.conn.execute("SELECT * FROM readers WHERE id = ?", (reader_id,)).fetchone()
        if row:
            r = Reader(row[1], row[2], row[3])
            r.id = row[0]
            r.registration_date = datetime.fromisoformat(row[4])
            return r
        return None

    def get_all_readers(self) -> list[Reader]:
        rows = self.conn.execute("SELECT * FROM readers").fetchall()
        result = []
        for r in rows:
            rd = Reader(r[1], r[2], r[3])
            rd.id = r[0]
            rd.registration_date = datetime.fromisoformat(r[4])
            result.append(rd)
        return result

    def update_reader(self, reader_id, **kwargs) -> bool:
        r = self.get_reader_by_id(reader_id)
        if not r:
            return False
        if "name" in kwargs: r.name = kwargs["name"]
        if "email" in kwargs: r.email = kwargs["email"]
        if "phone" in kwargs: r.phone = kwargs["phone"]
        self.conn.execute("UPDATE readers SET name=?, email=?, phone=?, registration_date=? WHERE id=?", (r.name, r.email, r.phone, r.registration_date.isoformat(), reader_id))
        self.conn.commit()
        return True

    def delete_reader(self, reader_id) -> bool:
        c = self.conn.execute("DELETE FROM readers WHERE id = ?", (reader_id,))
        self.conn.commit()
        return c.rowcount > 0

    def add_loan(self, loan: Loan) -> int:
        c = self.conn.execute("INSERT INTO loans (book_id, reader_id, loan_date, return_date, is_returned) VALUES (?, ?, ?, ?, ?)", (loan.book_id, loan.reader_id, loan.loan_date.isoformat(), loan.return_date.isoformat(), int(loan.is_returned)))
        self.conn.commit()
        return c.lastrowid

    def get_loan_by_id(self, loan_id) -> Loan | None:
        row = self.conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
        if row:
            l = Loan(row[1], row[2], datetime.fromisoformat(row[3]), datetime.fromisoformat(row[4]))
            l.id = row[0]
            l.is_returned = bool(row[5])
            return l
        return None

    def get_all_loans(self) -> list[Loan]:
        rows = self.conn.execute("SELECT * FROM loans").fetchall()
        result = []
        for r in rows:
            l = Loan(r[1], r[2], datetime.fromisoformat(r[3]), datetime.fromisoformat(r[4]))
            l.id = r[0]
            l.is_returned = bool(r[5])
            result.append(l)
        return result

    def update_loan(self, loan_id, **kwargs) -> bool:
        l = self.get_loan_by_id(loan_id)
        if not l:
            return False
        if "book_id" in kwargs: l.book_id = kwargs["book_id"]
        if "reader_id" in kwargs: l.reader_id = kwargs["reader_id"]
        if "loan_date" in kwargs: l.loan_date = kwargs["loan_date"]
        if "return_date" in kwargs: l.return_date = kwargs["return_date"]
        if "is_returned" in kwargs: l.is_returned = kwargs["is_returned"]
        self.conn.execute("UPDATE loans SET book_id=?, reader_id=?, loan_date=?, return_date=?, is_returned=? WHERE id=?", (l.book_id, l.reader_id, l.loan_date.isoformat(), l.return_date.isoformat(), int(l.is_returned), loan_id))
        self.conn.commit()
        return True

    def get_reader_loans(self, reader_id) -> list[Loan]:
        rows = self.conn.execute("SELECT * FROM loans WHERE reader_id = ?", (reader_id,)).fetchall()
        result = []
        for r in rows:
            l = Loan(r[1], r[2], datetime.fromisoformat(r[3]), datetime.fromisoformat(r[4]))
            l.id = r[0]
            l.is_returned = bool(r[5])
            result.append(l)
        return result

    def get_overdue_loans(self) -> list[Loan]:
        rows = self.conn.execute("SELECT * FROM loans WHERE is_returned = 0 AND return_date < ?", (datetime.now().isoformat(),)).fetchall()
        result = []
        for r in rows:
            l = Loan(r[1], r[2], datetime.fromisoformat(r[3]), datetime.fromisoformat(r[4]))
            l.id = r[0]
            l.is_returned = bool(r[5])
            result.append(l)
        return result
