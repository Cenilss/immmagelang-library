import json
from datetime import datetime

DB_FILE = "database.json"

def load_data():
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=2)

def add_book(inventory_number, title, author):
    data = load_data()
    new_id = max([book["id"] for book in data["books"]], default=0) + 1
    data["books"].append({
        "id": new_id,
        "inventory_number": inventory_number,
        "title": title,
        "author": author,
        "available": True,
        "borrower": "",
        "borrow_date": ""
    })
    save_data(data)

def borrow_book(book_id, borrower, date):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id and book["available"]:
            book["available"] = False
            book["borrower"] = borrower
            book["borrow_date"] = date
            break
    save_data(data)

def return_book(book_id):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id and not book["available"]:
            book["available"] = True
            book["borrower"] = ""
            book["borrow_date"] = ""
            break
    save_data(data)
