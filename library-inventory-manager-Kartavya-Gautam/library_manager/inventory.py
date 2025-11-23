from pathlib import Path
from .book import Book

class LibraryInventory:
    def __init__(self, filename="books.txt"):
        self.filename = Path(filename)
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        return [b for b in self.books if b.isbn == isbn]

    def display_all(self):
        if not self.books:
            print("No books in library yet.")
        else:
            for b in self.books:
                print(b)

    def load_from_file(self):
        try:
            if not self.filename.exists():
                return

            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(" | ")
                    if len(parts) == 4:
                        title, author, isbn, status = parts
                        self.books.append(Book(title, author, isbn, status))

        except:
            print("Could not load saved data.")

    def save_to_file(self):
        try:
            with open(self.filename, "w") as f:
                for b in self.books:
                    f.write(f"{b.title} | {b.author} | {b.isbn} | {b.status}\n")

        except:
            print("Could not save data.")
