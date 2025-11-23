# 📚 Library Inventory Manager

This mini project is a simple **command-line Library Inventory Manager** built using Python.  
It allows a library to store book details, issue and return books, and save the data in a text file so the records stay saved even after closing the program.

This project uses **Object-Oriented Programming (OOP)** and a **menu-driven interface**, and is organized into multiple files and folders for better structure.

---

## ✅ What I Built

In this project, I created:

- A `Book` class to store book information
- A `LibraryInventory` class to manage all books
- A menu system for user interaction
- Text file storage (`books.txt`) to save data
- Exception handling for file loading and issuing/returning books
- Proper folder structure using packages

---

## ✅ Features of My Program

- Add new books
- Issue a book
- Return a book
- View all books
- Search books by title
- Data saved in `books.txt`
- Loads previous data automatically when program starts

---
## Project Structure

library_inventory_project/
│
├── library_manager/
│ ├── init.py
│ ├── book.py
│ └── inventory.py
│
├── cli/
│ └── main.py
│
├── books.txt
├── README.md
└── requirements.txt


- `library_manager/` : Package containing `Book` and `LibraryInventory` classes.
- `cli/` : Contains the `main.py` CLI interface.
- `books.txt` : Stores the current book catalog in text format.
- `README.md` : This documentation file.
- `requirements.txt` : Lists project dependencies (none external for this project).

---
## Usage Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/kartavya79/Python_Assignment/Liberary_inventory_managaer-Kartavya-Gautam.git
cd Liberary_inventory_managaer-Kartavya-Gautam/-yourname
python cli/main.py

```

<img width="873" height="662" alt="image" src="https://github.com/user-attachments/assets/286e4c50-b0ac-4206-a402-0ccbb0353a70" />

