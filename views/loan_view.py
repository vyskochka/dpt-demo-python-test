# Здесь должно быть представление для работы с займами согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class LoanView(ttk.Frame):
    def __init__(self, parent, loan_controller, book_controller, reader_controller) -> None:
        super().__init__(parent)
        self.controller = loan_controller
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_loans()

    def create_widgets(self) -> None:
        frame = ttk.LabelFrame(self, text="Создать выдачу")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="ID книги:").grid(row=0, column=0, sticky="w")
        self.book_id_entry = ttk.Entry(frame)
        self.book_id_entry.grid(row=0, column=1)

        ttk.Label(frame, text="ID читателя:").grid(row=1, column=0, sticky="w")
        self.reader_id_entry = ttk.Entry(frame)
        self.reader_id_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Дней на возврат:").grid(row=2, column=0, sticky="w")
        self.days_entry = ttk.Entry(frame)
        self.days_entry.grid(row=2, column=1)
        self.days_entry.insert(0, "14")

        ttk.Button(frame, text="Создать", command=self.create_loan).grid(row=3, column=0, columnspan=2)

        self.tree = ttk.Treeview(self, columns=("ID", "BookID", "ReaderID", "LoanDate", "ReturnDate", "Returned"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("BookID", text="ID книги")
        self.tree.heading("ReaderID", text="ID читателя")
        self.tree.heading("LoanDate", text="Дата выдачи")
        self.tree.heading("ReturnDate", text="Дата возврата")
        self.tree.heading("Returned", text="Возвращена")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Button(self, text="Вернуть выбранное", command=self.return_selected).pack(pady=5)

    def refresh_loans(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for loan in self.controller.get_all_loans():
            returned = "Да" if loan.is_returned else "Нет"
            self.tree.insert("", "end", values=(loan.id, loan.book_id, loan.reader_id, loan.loan_date.strftime("%Y-%m-%d"), loan.return_date.strftime("%Y-%m-%d"), returned))

    def create_loan(self) -> None:
        book_id = self.book_id_entry.get()
        reader_id = self.reader_id_entry.get()
        days = self.days_entry.get()
        if book_id and reader_id and days:
            loan_date = datetime.now()
            return_date = loan_date + timedelta(days=int(days))
            self.controller.create_loan(int(book_id), int(reader_id), loan_date, return_date)
            self.refresh_loans()

    def return_selected(self) -> None:
        selected = self.tree.selection()
        if selected:
            loan_id = self.tree.item(selected[0])["values"][0]
            self.controller.return_book(loan_id)
            self.refresh_loans()
