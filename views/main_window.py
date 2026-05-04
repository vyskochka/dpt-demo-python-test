# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk
from views.book_view import BookView
from views.reader_view import ReaderView
from views.loan_view import LoanView

class MainWindow(tk.Tk):
    def __init__(self, book_controller, reader_controller, loan_controller) -> None:
        super().__init__()
        self.title("Библиотека")
        self.geometry("700x500")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.book_view = BookView(notebook, book_controller)
        self.reader_view = ReaderView(notebook, reader_controller)
        self.loan_view = LoanView(notebook, loan_controller, book_controller, reader_controller)

        notebook.add(self.book_view, text="Книги")
        notebook.add(self.reader_view, text="Читатели")
        notebook.add(self.loan_view, text="Выдачи")
