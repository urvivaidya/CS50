import os
import sqlite3

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///library.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show list of users books along with its status"""
    # create variable for storing the user
    current_user = session["user_id"]

    #query for the books borrowed
    borrowed = db.execute("SELECT  books.title, authors.name, books.isbn, borrowers.name AS nameBorrower, borrowers.contact FROM books\
        JOIN authors ON books.author_id = authors.id JOIN library ON library.book_id = books.book_id JOIN borrowings \
        ON borrowings.library_id = library.library_id JOIN borrowers ON  borrowings.borrower_id = borrowers.id JOIN users\
        ON library.user_id = users.id WHERE users.id =?", current_user)

    # query for the books available in the users library
    library_display = db.execute("SELECT  books.title, authors.name, books.isbn FROM books JOIN authors ON\
        books.author_id = authors.id JOIN library ON library.book_id = books.book_id WHERE user_id =? ORDER BY title", current_user)

    return render_template("index.html", total=len(library_display), borrowed=borrowed, libraryAll=library_display)


@app.route("/lend", methods=["GET", "POST"])
@login_required
def lend():
    """Add borrowers + lend and return books using separate functions"""
    current_user = session["user_id"]
    # display books that are available for lending along with borrowers
    BOOKS = []
    user_books = db.execute(
        "SELECT title FROM books WHERE book_id IN (SELECT book_id FROM library WHERE user_id=? AND availability =?)\
        ORDER BY title", current_user, True)
    for i in range(len(user_books)):
        title = user_books[i]["title"]
        BOOKS.append(title)

    BORROWERS = []
    borrowers = db.execute("SELECT name FROM borrowers WHERE user_id=?", current_user)
    for i in range(len(borrowers)):
        name = borrowers[i]["name"]
        BORROWERS.append(name)

    # display books that are already lent so that they can be marked as returned
    LENT_BOOKS = []
    lent_books = db.execute(
        "SELECT title FROM books WHERE book_id IN(SELECT book_id FROM library WHERE availability =? AND user_id=?) \
        ORDER BY title", False, current_user)
    for i in range(len(lent_books)):
        title = lent_books[i]["title"]
        LENT_BOOKS.append(title)
    return render_template("lend.html", title=BOOKS, name=BORROWERS, lent_title=LENT_BOOKS)


# adding borrower to users db
@app.route("/add_borrower", methods=["GET", "POST"])
@login_required
def add_borrower():
    current_user = session["user_id"]
    # if borrower not in db add borrower
    name = request.form.get("borrower").strip().upper()
    contact = request.form.get("contact").strip().upper()
    try:
        db.execute("INSERT INTO borrowers (name, contact, user_id) VALUES(?,?,?)", name, contact, current_user)
        flash('borrower successfully added')
        return redirect("/lend")
    except ValueError:
        flash('borrower already exists')
        return render_template("lend.html")


# allowing user to lend a book
@app.route("/lend_book", methods=["GET", "POST"])
@login_required
def lend_book():
    current_user = session["user_id"]
    title = request.form.get("book")
    borrower_name = request.form.get("borrower")

    # get the library id and borrower id to update the borrowings table and availability of the book
    book_id = db.execute("SELECT book_id FROM books WHERE title=?", title)
    library_id = db.execute("SELECT library_id FROM library WHERE book_id=? AND user_id=?", book_id[0]["book_id"], current_user)
    borrower = db.execute("SELECT id FROM borrowers WHERE name=? AND user_id=?", borrower_name, current_user)

    # add the user's book data and borrower's id the borrowings table
    db.execute("INSERT INTO borrowings (library_id, borrower_id) VALUES (?,?)", library_id[0]["library_id"], borrower[0]["id"])

    # update the users library and mark the book as unavailable/borrowed
    db.execute("UPDATE library SET availability=? WHERE user_id=? AND book_id=?", False, current_user, book_id[0]["book_id"])

    flash('book lent')
    return render_template("lend.html")


# allow users to return books already lent
@app.route("/return_book", methods=["GET", "POST"])
@login_required
def return_book():
    current_user = session["user_id"]
    book = request.form.get("book")
    # get book id to update availability and library_id to update borrowings
    book_id = db.execute("SELECT book_id FROM books WHERE title=?", book)
    library_id = db.execute("SELECT library_id FROM library WHERE book_id=? AND user_id=?", book_id[0]["book_id"], current_user)

    # update the books availability and borrowings table
    db.execute("DELETE FROM borrowings WHERE library_id=?", library_id[0]["library_id"])
    db.execute("UPDATE library SET availability=? WHERE user_id=? AND book_id=?", True, current_user, book_id[0]["book_id"])
    flash('book returned')
    return render_template("lend.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """allow users to add books"""
    if request.method == "GET":
        current_user = session["user_id"]
        # display books that are already lent so that they can be marked as returned
        MY_BOOKS = []
        my_books = db.execute(
            "SELECT title FROM books WHERE book_id IN(SELECT book_id FROM library WHERE availability =? \
            AND user_id=?) ORDER BY title", True, current_user)
        for i in range(len(my_books)):
            title = my_books[i]["title"]
            MY_BOOKS.append(title)
        return render_template("add.html", my_books=MY_BOOKS)
    else:
        current_user = session["user_id"]
        title = request.form.get("title").strip().upper()
        author = request.form.get("author").strip().upper()
        isbn = request.form.get("isbn").strip().upper()

        # check if book and author already exist if not add them
        db.execute("INSERT OR IGNORE INTO authors(name) VALUES(?)", author)
        author_id = db.execute("SELECT id from authors WHERE name =?", author)
        db.execute("INSERT OR IGNORE INTO books(title, author_id) VALUES(?,?)", title, author_id[0]["id"])
        book_id = db.execute("SELECT book_id FROM books WHERE title=? and author_id=?", title, author_id[0]["id"])

        # check if user book already exists else add it
        try:
            db.execute("INSERT INTO library (book_id, user_id) VALUES(?,?)", book_id[0]["book_id"], current_user)
            flash('successfully added')
            return render_template("add.html")
        except ValueError:
            flash('book already exists')
            return render_template("add.html")


@app.route("/delete_book", methods=["GET", "POST"])
@login_required
def deleteBook():

    current_user = session["user_id"]
    title = request.form.get("book")

    # get the book_id
    book_id = db.execute("SELECT book_id FROM books WHERE title=?", title)

    # delete book from users library
    db.execute("DELETE FROM library WHERE book_id=? AND user_id=?", book_id[0]["book_id"], current_user)
    flash('book deleted')
    return render_template("add.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # get the username and password from the form in register.html
    if request.method == "POST":

        # check if username already exists and return apology if it does
        check_username = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if check_username:
            return apology("username not available")

        # ensure passwords match
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match")

        # hash the users password
        password_hash = generate_password_hash(request.form.get("password"))
        # register the user and enter their details in the finance database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), password_hash)
        # Redirect user to home page
        return redirect("/login")
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
