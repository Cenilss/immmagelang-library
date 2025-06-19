import json
import os

DB_FILE = "database.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"books": []}, f)

def load_books():
    with open(DB_FILE, "r") as f:
        return json.load(f)["books"]

def save_books(books):
    with open(DB_FILE, "w") as f:
        json.dump({"books": books}, f, indent=2)

def add_book(inv, title, author):
    books = load_books()

    # Cek apakah nomor inventaris sudah digunakan
    if any(book["inventory_number"] == inv for book in books):
        raise ValueError("Nomor inventaris sudah digunakan.")

    new_id = max([b["id"] for b in books], default=0) + 1
    books.append({
        "id": new_id,
        "inventory_number": inv,
        "title": title,
        "author": author,
        "available": True,
        "borrower": "",
        "borrow_date": ""
    })
    save_books(books)

def borrow_book(book_id, borrower, date):
    books = load_books()
    for b in books:
        if b["id"] == book_id and b["available"]:
            b["available"] = False
            b["borrower"] = borrower
            b["borrow_date"] = date
    save_books(books)

def return_book(book_id):
    books = load_books()
    for b in books:
        if b["id"] == book_id and not b["available"]:
            b["available"] = True
            b["borrower"] = ""
            b["borrow_date"] = ""
    save_books(books)

def find_by_inventory(inv_number):
    books = load_books()
    for b in books:
        if b["inventory_number"] == inv_number:
            return b
    return None

def delete_book(book_id):
    books = load_books()
    books = [b for b in books if b["id"] != book_id]
    save_books(books)
