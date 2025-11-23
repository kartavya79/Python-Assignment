import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library_manager import Book, LibraryInventory


def menu():
    print("\n--- Library Menu ---")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
    return input("Choose: ")

def main():
    inventory = LibraryInventory()
    inventory.load_from_file()

    while True:
        choice = menu()

        if choice == "1":
            inventory.add_book(Book(
                input("Title: "),
                input("Author: "),
                input("ISBN: ")
            ))
            print("Book added.")

        elif choice == "2":
            isbn = input("ISBN: ")
            books = inventory.search_by_isbn(isbn)
            if books:
                try:
                    books[0].issue()
                    print("Issued.")
                except Exception as e:
                    print(e)
            else:
                print("Not found.")

        elif choice == "3":
            isbn = input("ISBN: ")
            books = inventory.search_by_isbn(isbn)
            if books:
                try:
                    books[0].return_book()
                    print("Returned.")
                except Exception as e:
                    print(e)
            else:
                print("Not found.")

        elif choice == "4":
            inventory.display_all()

        elif choice == "5":
            title = input("Title: ")
            results = inventory.search_by_title(title)
            if results:
                for b in results:
                    print(b)
            else:
                print("No match.")

        elif choice == "6":
            inventory.save_to_file()
            print("Saved. Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
