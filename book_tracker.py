import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "books.json"

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("700x500")

        # Загрузка данных
        self.books = self.load_books()

        # Создание виджетов
        self.create_widgets()
        self.update_treeview()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = tk.Entry(self.root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(self.root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.pages_entry = tk.Entry(self.root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить книгу", command=self.add_book).grid(row=4, columnspan=2, pady=10)

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.grid(row=5, columnspan=2, pady=10)

        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side="left")
        self.filter_genre = tk.Entry(filter_frame, width=20)
        self.filter_genre.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Страниц >").pack(side="left")
        self.filter_pages = tk.Entry(filter_frame, width=6)
        self.filter_pages.pack(side="left", padx=2)

        tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).pack(side="left", padx=10)

        # Таблица (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("title", "author", "genre", "pages"), show='headings')
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        self.tree.column("pages", width=80)
        self.tree.grid(row=6, columnspan=2, sticky="nsew", padx=10)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages_str:
            messagebox.showerror("Ошибка", "Все поля обязательны!")
            return

        if not pages_str.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        pages = int(pages_str)

        self.books.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        })

        self.save_books()
        self.update_treeview()

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        try:
            pages_filter = int(self.filter_pages.get())
            if pages_filter < 0:
                pages_filter = 0
                messagebox.showwarning("Предупреждение", "Число страниц не может быть отрицательным. Установлено 0.")
                self.filter_pages.delete(0, tk.END)
                self.filter_pages.insert(0, "0")
                return False
            return True
        except ValueError:
            pages_filter = None

        filtered_books = []

        for book in self.books:
            match_genre = genre_filter == "" or genre_filter in book["genre"].lower()
            match_pages = pages_filter is None or book["pages"] > pages_filter

            if match_genre and match_pages:
                filtered_books.append(book)

        self.update_treeview(filtered_books)

    def update_treeview(self, books=None):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if books is None:
            books_to_show = self.books
        else:
            books_to_show = books

        for book in books_to_show:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def save_books(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_books(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
