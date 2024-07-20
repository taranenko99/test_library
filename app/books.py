import os
import json


class Book:
    def __init__(
        self, id: int, title: str, author: str, year: int, status: str
    ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status


class Library:
    def __init__(self, path_to_books_storage: str) -> None:
        self.books_storage = path_to_books_storage
        self.books = {}
        self.id = 1
        self.load_books()

    def load_books(self):
        if os.path.exists(self.books_storage):
            with open(self.books_storage, "r", encoding='utf-8') as f:
                books_data = json.load(f)
                for book_data in books_data:
                    book = Book(**book_data)
                    self.books[book.id] = book
                if self.books:
                    self.id = max(self.books.keys()) + 1
        else:
            with open(self.books_storage, "w", encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def save_books(
        self,
    ):
        with open(self.books_storage, "w", encoding='utf-8') as f:
            books_data = [book.__dict__ for book in self.books.values()]
            json.dump(books_data, f, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int):

        new_book = Book(
            self.id, title=title, author=author, year=year, status="В наличии"
        )
        self.books[self.id] = new_book
        self.id += 1
        self.save_books()

    def del_book(self, book_id: int):
        if book_id in self.books:
            title = self.books[book_id].title
            del self.books[book_id]
            self.save_books()

            return title

    def search_books(self, title: str = None, author: str = None, year: int = None):
        results = []
        for book in self.books.values():
            if (
                (title and title.lower() in book.title.lower())
                or (author and author.lower() in book.author.lower())
                or (year and book.year == year)
            ):
                results.append(book)

        return results
    
    def change_status_book(self, book_id: int, status: str):
        if book_id in self.books:
            if status not in ["В наличии", "Выдана"]:
                raise ValueError("Статус должен быть 'В наличии' или 'Выдана'")
            self.books[book_id].status = status
            self.save_books()              
        else:
            print("Книга с указанным ID ненайдена")
            
    def get_book_info(self, book_id: int):
        if book_id in self.books: 
            status = self.books[book_id].status
            title = self.books[book_id].title
            
            return status, title
        
    def get_books(self, page: int = 1, per_page: int = 5):
        start = (page - 1) * per_page
        end = start + per_page
        books_list = list(self.books.values())
        
        return books_list[start:end]
