import os
from app.books import Library


def __info():
    print(
        """Вам доступны следующие возможности: \n
          1. Посмотреть все доступные книги.
          2. Добавить новую книгу.
          3. Удалить книгу.
          4. Найти книгу.
          5. Изменить статус книги.
          """
    )


def display_books(library: Library, page: int):
    books = library.get_books(page)
    if page == 1 and not books:
        print("Библиотека пуста")
    elif not books:
        print("Нет книг на этой странице.")
    else:
        for book in books:
            print(
                f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}"
            )
    print(
        "\nКоманды для навигации:\nN - следующая страница\nP - предыдущая страница\nQ - выход"
    )


def main():
    library = Library(os.path.join(os.getcwd(), "database", "books.json"))
    print("Добро пожаловать в библиотеку", end="\n")
    __info()

    while True:
        command = input("Пожалуйста введите желаемый номер запроса: ")

        if command == "1":
            page = 1
            while True:
                display_books(library, page)
                nav_command = input("Введите команду для навигации: ").strip().upper()
                if nav_command == "N":
                    page += 1
                elif nav_command == "P" and page > 1:
                    page -= 1
                elif nav_command == "Q":
                    break
                else:
                    print("Неверная команда навигации. Попробуйте снова.")
            __info()

        elif command == "2":
            title = input("Введите заголовок книги: ").strip()
            author = input("Введите автора книги: ").strip()
            year = input("Введите год книги: ").strip()

            if title and author and year:
                try:
                    year = int(year)
                    library.add_book(title, author, year)
                    print(f"Книга '{title}' успешно добавлена.")
                    __info()
                except ValueError:
                    print("Год должен быть числом.")
                    __info()

        elif command == "3":
            try:
                book_id = int(
                    input("Введите id книги которую хотите удалить: ").strip()
                )
                title = library.del_book(book_id)
                if title:
                    print(f"Книга '{title}' была удалена.")
                    __info()
                else:
                    print("Книга с указанным ID не найдена.")
                    __info()
            except ValueError:
                print("ID должен быть числом.")
                __info()

        elif command == "4":
            print(
                """Выберете фильтры по которым вы хотите найти книги:
                1. Заголовок
                2. Автор
                3. Год
                
                Если собираетесь использовать несколько фильтров укажите их через запятую.
                  """
            )

            filters = input("Укажите номера фильтров для поиска: ").strip().split(",")
            search_params = {}
            if "1" in filters:
                search_params["title"] = input("Введите заголовок для поиска: ").strip()
            if "2" in filters:
                search_params["author"] = input("Введите автора для поиска: ").strip()
            if "3" in filters:
                search_year = input("Введите год для поиска: ").strip()
                try:
                    search_params["year"] = int(search_year)
                except ValueError:
                    print("Год должен быть числом.")
                    __info()
            results = library.search_books(**search_params)
            if results:
                for book in results:
                    print(
                        f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}"
                    )
                    __info()
            else:
                print("Книги не найдены.")
                __info()

        elif command == "5":
            try:
                book_id = int(input("Введите ID книги: ").strip())
                prev_status, title = library.get_book_info(book_id)
                if title is None:
                    print("Книга с указанным ID не найдена.")
                    continue

                print(f"Статус книги '{title}': '{prev_status}'")

                if prev_status == "В наличии":
                    status_response = (
                        input(
                            "Хотите изменить статус на 'Выдана'? Введите 'да' или 'нет': "
                        )
                        .strip()
                        .lower()
                    )
                    if status_response == "да":
                        library.change_status_book(book_id, "Выдана")
                        print(
                            f"Статус книги '{title}' был изменен c '{prev_status}' на 'Выдана'"
                        )
                    else:
                        print("Статус книги не был изменен.")
                    __info()
                elif prev_status == "Выдана":
                    status_response = (
                        input(
                            "Хотите изменить статус на 'В наличии'? Введите 'да' или 'нет': "
                        )
                        .strip()
                        .lower()
                    )
                    if status_response == "да":
                        library.change_status_book(book_id, "В наличии")
                        print(
                            f"Статус книги '{title}' был изменен c '{prev_status}' на 'В наличии'"
                        )
                    else:
                        print("Статус книги не был изменен.")
                    __info()
            except ValueError:
                print("ID должен быть числом.")

        else:
            print("Неверная команда. Попробуйте снова.")
            __info()


if __name__ == "__main__":
    main()
