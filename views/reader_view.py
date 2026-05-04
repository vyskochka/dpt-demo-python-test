# Здесь должно быть представление для работы с читателями согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox

class ReaderView(ttk.Frame):
    def __init__(self, parent, reader_controller) -> None:
        super().__init__(parent)
        self.controller = reader_controller
        self.create_widgets()
        self.refresh_readers()

    def create_widgets(self) -> None:
        frame = ttk.LabelFrame(self, text="Добавить читателя")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Имя:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_entry = ttk.Entry(frame)
        self.email_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Телефон:").grid(row=2, column=0, sticky="w")
        self.phone_entry = ttk.Entry(frame)
        self.phone_entry.grid(row=2, column=1)

        ttk.Button(frame, text="Добавить", command=self.add_reader).grid(row=3, column=0, columnspan=2)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Email", "Phone"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Телефон")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Button(self, text="Удалить выбранное", command=self.delete_selected).pack(pady=5)

    def refresh_readers(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for reader in self.controller.get_all_readers():
            self.tree.insert("", "end", values=(reader.id, reader.name, reader.email, reader.phone))

    def add_reader(self) -> None:
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        if name and email and phone:
            self.controller.add_reader(name, email, phone)
            self.refresh_readers()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if selected:
            reader_id = self.tree.item(selected[0])["values"][0]
            self.controller.delete_reader(reader_id)
            self.refresh_readers()
