# Здесь должен быть контроллер для работы с займами согласно README.md

from models.loan import Loan
from datetime import datetime

class LoanController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def create_loan(self, book_id, reader_id, loan_date, return_date) -> int:
        loan = Loan(book_id, reader_id, loan_date, return_date)
        book = self.db.get_book_by_id(book_id)
        if book and book.available > 0:
            book.available -= 1
            self.db.update_book(book_id, available=book.available)
            return self.db.add_loan(loan)
        return -1

    def get_loan(self, loan_id) -> Loan | None:
        return self.db.get_loan_by_id(loan_id)

    def get_all_loans(self) -> list[Loan]:
        return self.db.get_all_loans()

    def return_book(self, loan_id) -> bool:
        loan = self.db.get_loan_by_id(loan_id)
        if loan and not loan.is_returned:
            loan.is_returned = True
            self.db.update_loan(loan_id, is_returned=True)
            book = self.db.get_book_by_id(loan.book_id)
            if book:
                book.available += 1
                self.db.update_book(book.id, available=book.available)
            return True
        return False

    def get_overdue_loans(self) -> list[Loan]:
        return self.db.get_overdue_loans()

    def get_reader_loans(self, reader_id) -> list[Loan]:
        return self.db.get_reader_loans(reader_id)
