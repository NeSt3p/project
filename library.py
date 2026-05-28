# Проект: Система учета библиотеки
# В программе реализовано:
# 1) хранение книг
# 2) хранение читателей
# 3) выдача и возврат книг
# 4) сохранение данных в файл (JSON)
# 5) консольный интерфейс
# 6) используются принципы ООП: работа с классами

import json

class Book: #класс книги
    def __init__(self, title, author): #создаем книгу
        self.title = title #название книги
        self.author = author #автор книги
        self.taken = False #выдана книга или нет

class Reader: #класс читателя
    def __init__(self, name): #создаем читателя
        self.name = name #имя читателя
        self.books = [] #список книг читателя

class Library: #класс библиотеки
    def __init__(self): #создаем библиотеку
        self.books = [] #список книг
        self.readers = [] #список читателей

    def add_book(self, title, author): #добавление книги
        book = Book(title, author) #создаем объект книги
        self.books.append(book) #добавляем книгу в список
        print("Книга добавлена!")

    def show_books(self): #показать книги
        if len(self.books) == 0: #если книг нет
            print("Книг нет(")
            return

        for book in self.books: #перебираем книги
            if book.taken == True: #проверяем статус книги
                status = "Выдана"
            else:
                status = "Свободна"

            #вывод информации о книге
            print(book.title, "-", book.author, "-", status)

    def add_reader(self, name): #добавление читателя
        reader = Reader(name) #создаем объект читателя
        self.readers.append(reader) #добавляем читателя в список
        print("Читатель добавлен!")

    def show_readers(self): #показать читателей
        if len(self.readers) == 0: #если читателей нет
            print("Читателей нет(")
            return

        #выводим читателей
        for reader in self.readers:
            print(reader.name)

    
    def give_book(self, title, reader_name): #выдача книги
        for book in self.books: #ищем книгу
            if book.title == title: #если нашли книгу
                if book.taken == True: #если книга уже выдана
                    print("Книга уже выдана!")
                    return

                for reader in self.readers: #ищем читателя
                    if reader.name == reader_name: #если нашли читателя
                        book.taken = True #книга становится выданной
                        reader.books.append(title) #добавляем книгу читателю
                        print("Книга выдана!")
                        return
        print("Ошибка(")

    def return_book(self, title, reader_name): #возврат книги
        for book in self.books: #ищем книгу
            if book.title == title: #если нашли книгу
                for reader in self.readers: #ищем читателя
                    if reader.name == reader_name: #если нашли читателя
                        book.taken = False #книга становится свободной
                        if title in reader.books: #удаляем книгу у читателя
                            reader.books.remove(title)
                        print("Книга возвращена!")
                        return
        print("Ошибка(")

    def save_data(self): #сохранение данных в файл
        data = {
            "books": [], #создаем словарь для книг
            "readers": [] #создаем словарь для читателя
        }

        for book in self.books: #сохраняем книги
            data["books"].append({
                "title": book.title,
                "author": book.author,
                "taken": book.taken
            })

        for reader in self.readers: #сохраняем читателей
            data["readers"].append({
                "name": reader.name,
                "books": reader.books
            })

        file = open("library.json", "w", encoding="utf-8") #открываем файл
        json.dump(data, file, ensure_ascii=False) #записываем данные в файл
        file.close() #закрываем файл
        print("Данные сохранены!")

    def load_data(self): #загрузка данных из файла
        try:
            file = open("library.json", "r", encoding="utf-8") #открываем файл
            data = json.load(file) #загружаем данные
            file.close() #закрываем файл

            #очищаем старые данные
            self.books = []
            self.readers = []

            for item in data["books"]: #загружаем книги
                book = Book(item["title"], item["author"]) #создаем книгу
                book.taken = item["taken"] #загружаем статус книги
                self.books.append(book) #добавляем книгу в список

            for item in data["readers"]: #загружаем читателей
                reader = Reader(item["name"]) #создаем читателя
                reader.books = item["books"] #загружаем список книг
                self.readers.append(reader) #добавляем читателя в список
            print("Данные загружены!")
        except:
            print("Файл не найден")

#создаем библиотеку
library = Library()

#делаем консольное меню
while True:
    print("\n1. Добавить книгу")
    print("2. Показать книги")
    print("3. Добавить читателя")
    print("4. Показать читателей")
    print("5. Выдать книгу")
    print("6. Вернуть книгу")
    print("7. Сохранить")
    print("8. Загрузить")
    print("0. Выход")
    choice = input("Выберите действие: ")

    #добавление книги
    if choice == "1":
        title = input("Введите название книги: ")
        author = input("Введите автора: ")
        library.add_book(title, author)

    #показать книги
    elif choice == "2":
        library.show_books()

    #добавление читателя
    elif choice == "3":
        name = input("Введите имя читателя: ")
        library.add_reader(name)

    #показать читателей
    elif choice == "4":
        library.show_readers()

    #выдача книги
    elif choice == "5":
        title = input("Введите название книги: ")
        name = input("Введите имя читателя: ")
        library.give_book(title, name)

    #возврат книги
    elif choice == "6":
        title = input("Введите название книги: ")
        name = input("Введите имя читателя: ")
        library.return_book(title, name)

    #сохранение
    elif choice == "7":
        library.save_data()

    #загрузка
    elif choice == "8":
        library.load_data()

    #выход
    elif choice == "0":
        print("Программа завершена!")
        break
        
    #ошибка
    else:
        print("Неверный ввод!!")
