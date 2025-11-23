class Book:
    # simple class to store book info
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} ({self.isbn}) by {self.author} - {self.status}"

    def is_available(self):
        return self.status == "available"

    def issue(self):
        if not self.is_available():
            raise Exception("Book already issued.")
        self.status = "issued"

    def return_book(self):
        if self.is_available():
            raise Exception("Book is already in library.")
        self.status = "available"

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
