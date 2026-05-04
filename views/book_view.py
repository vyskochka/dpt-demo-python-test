# Здесь должно быть представление для работы с книгами согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox

class BookView(ttk.Frame):
    def __init__(self, parent, book_controller) -> None:
        super().__init__(parent)
        self.controller = book_controller
        self.create_widgets()
        self.refresh_books()

    def create_widgets(self) -> None:
        frame = ttk.LabelFrame(self, text="Добавить книгу")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(frame)
        self.title_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_entry = ttk.Entry(frame)
        self.author_entry.grid(row=1, column=1)

        ttk.Label(frame, text="ISBN:").grid(row=2, column=0, sticky="w")
        self.isbn_entry = ttk.Entry(frame)
        self.isbn_entry.grid(row=2, column=1)

        ttk.Label(frame, text="Год:").grid(row=3, column=0, sticky="w")
        self.year_entry = ttk.Entry(frame)
        self.year_entry.grid(row=3, column=1)

        ttk.Label(frame, text="Количество:").grid(row=4, column=0, sticky="w")
        self.quantity_entry = ttk.Entry(frame)
        self.quantity_entry.grid(row=4, column=1)

        ttk.Button(frame, text="Добавить", command=self.add_book).grid(row=5, column=0, columnspan=2)

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Author", "ISBN", "Year", "Qty", "Avail"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Qty", text="Кол-во")
        self.tree.heading("Avail", text="Доступно")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Button(self, text="Удалить выбранное", command=self.delete_selected).pack(pady=5)

    def refresh_books(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in self.controller.get_all_books():
            self.tree.insert("", "end", values=(book.id, book.title, book.author, book.isbn, book.year, book.quantity, book.available))

    def add_book(self) -> None:
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        year = self.year_entry.get()
        quantity = self.quantity_entry.get()
        if title and author and isbn and year and quantity:
            self.controller.add_book(title, author, isbn, int(year), int(quantity))
            self.refresh_books()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if selected:
            book_id = self.tree.item(selected[0])["values"][0]
            self.controller.delete_book(book_id)
            self.refresh_books()
