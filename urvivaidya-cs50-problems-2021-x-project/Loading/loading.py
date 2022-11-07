import csv

from cs50 import SQL

db = SQL("sqlite:///library.db")


with open("library cs50.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        book = row[0].strip().upper()
        isbn = row[2].strip()
        name = row[1].strip().upper()
        db.execute("INSERT OR IGNORE INTO authors (name) VALUES(?)", name)
        author_id = db.execute("SELECT id FROM authors WHERE name=?", name)
        db.execute("INSERT OR IGNORE INTO books (title, isbn, author_id) VALUES(?, ?, ?)", book, isbn, author_id[0]["id"])
        book_id = db.execute("SELECT book_id FROM books WHERE title=?", book)
        db.execute("INSERT OR IGNORE INTO library (book_id, user_id) VALUES (?,?)", book_id[0]["book_id"], 1)