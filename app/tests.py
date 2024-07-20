import unittest
import os
import json
from books import Library

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.getcwd(), "test_database")
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_db_path = os.path.join(self.test_dir, "books.json")

        self.library = Library(self.test_db_path)

        self.library.add_book("Тестовая книга 1", "Автор 1", 2000)
        self.library.add_book("Тестовая книга 2", "Автор 2", 2005)
        self.library.add_book("Тестовая книга 3", "Автор 3", 2010)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_display_books(self):
        books_page_1 = self.library.get_books(1)
        self.assertEqual(len(books_page_1), 3)

    def test_add_book(self):
        initial_book_count = len(self.library.books)
        self.library.add_book("Новая книга", "Новый автор", 2022)
        self.assertEqual(len(self.library.books), initial_book_count + 1)

    def test_del_book(self):
        book_id_to_delete = list(self.library.books.keys())[0]
        title = self.library.del_book(book_id_to_delete)
        self.assertIsNotNone(title)
        self.assertNotIn(book_id_to_delete, self.library.books)

    def test_search_books(self):
        results_by_title = self.library.search_books(title="Тестовая книга 1")
        self.assertEqual(len(results_by_title), 1)
        self.assertEqual(results_by_title[0].title, "Тестовая книга 1")

        results_by_author = self.library.search_books(author="Автор 2")
        self.assertEqual(len(results_by_author), 1)
        self.assertEqual(results_by_author[0].author, "Автор 2")

        results_by_year = self.library.search_books(year=2010)
        self.assertEqual(len(results_by_year), 1)
        self.assertEqual(results_by_year[0].year, 2010)

    def test_change_status_book(self):
        book_id_to_change = list(self.library.books.keys())[0]
        prev_status, title = self.library.get_book_info(book_id_to_change)
        self.assertEqual(prev_status, "В наличии")

        self.library.change_status_book(book_id_to_change, "Выдана")
        new_status, _ = self.library.get_book_info(book_id_to_change)
        self.assertEqual(new_status, "Выдана")

        self.library.change_status_book(book_id_to_change, "В наличии")
        reverted_status, _ = self.library.get_book_info(book_id_to_change)
        self.assertEqual(reverted_status, "В наличии")

if __name__ == "__main__":
    unittest.main()
