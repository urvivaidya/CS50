# PERSONAL LIBRARY MANAGER

#### Video Demo:  [PERSONAL LIBRARY MANAGER](https://youtu.be/tVk6v-DJtQU)

#### Description:
I’m a voracious reader. You will find books stashed in my drawers, shelves, cupboards, even below my bed.

Not only do I love to read, I also love to encourage other people to pick up the habit. I am also very passionate

when it comes to expressing my obsession with books. Even to people I have just met.So the minute someone gets

interested in reading the book im blabbing on about I'm happily offering to lend them my copy, while instantly

regretting it internally. Don't get me wrong, I have no trouble sharing or lending my books, but I've been burned

in the past when I've lent out my beloved books only to never have them returned. Either its been too long and I dont

remember who I've loaned them to or even if I do, I've lost touch with the person somehow among myraid other reasons.

I hate losing copies like that. I even have a seal **_Urvi Vaidya's library_** which I have embossed into all my books

hoping whoever takes them feels bad enough to return them. Eventually I began keeping a record of my books in an excel

sheet. It is not just me who faces thse problems, I'm sure, every book hoarder out there has lost a beloved book just

like me at some point. So for my final project I decided to write a web application using Flask so that I could effetively

manage my book collection. I also took some inspiration from the finance problem set so that not just me but everyone who

wants it can use my programme to do the same. It allows the user to keep track of whom the book is lent to along with the

borrowers contact information. So now lets move on to the actual project.


```
On a side note I cheated and used code to update my own library using my aforementioned excel sheet. I downloaded the

sheet in a csv file and wrote a programme called loading.py to add the books to my own library catalogue.
```

```
1. Starting with the index template
   - I wanted to be able to have a tab on my inventory in general
   - The index allows the user to quickly have a view of the total number of books the user has and a list
     of the same. I was not sure how i wanted to display this information but eventually settled on an
     alphabetically ordered table.
   - Later on I decided to display the books that have checked out on the same page as well since that was the
     goal of the programme. I also chose to display the contact details in this table, because who hasnt lost
     contact details after a while.

 ![This is a alt text.](/image/index-home.png "homepage")

2. The second page is the add page(catalogue) which is essentially the page that allows the user to edit their
    own personal catalogue. The user can add books and delete books as needed. I kept both these functions on
    the same page as they ae related activities.The delete book has a convinient searchabel select menu.

 ![This is a alt text.](/image/catalogue.png "catalogue")

3. The third page is the update books page.
   - This page allows the user to add borrowers along with their contact so that the user can start lending books
   - It also allows the user to lend books to added borrowers. It also has a searchable select menu as well as a borrowers menu
   - Only books that have not been marked as borrowed are displayed in this list. Since it's a personal library
     I pre-suppose that the user has only the one copy.
   - The third part of my page is the return book page. The searchable select menu only displays books that have been
     checked-out/lent already.

 ![This is a alt text.](/image/edit-library.png "edit-library")

4. I will talk about the log-in and register page together
   - Similar to finance the user can only manage her library after registering and logging in.
   - I have used the template from the finance problem set and made it my own to cover my requirements.
   - It allows multiple people to use the programme to manage their libraries too and makes this application a service of sorts.

5. Coming to application.py \*- this is where the magic happens\* :stuck_out_tongue_winking_eye:. Jokes apart, this page is pretty
    self-explanatory. it runs all the other pages along with the database which we will talk about next.

6. Finally we talk about the database that stores all our information
   - The database took me the longest to design. I originally had just the four tables, for users, books, authors and library.
   - The book table would hold the essential information about the book and is linked to the author table. This way the author names are stored only once.
   - The original library table would essentially store all the users book information along with the link to the borrower but it got to messy
     too quickly.
   - To make the database more clean and scaleable I decided to split all the information and link it relationally using more tables.
   - the current db has the following tables : users, books, authors, library, borrowers and borrowings.
   - The current design stores the books and authors just once and allows multiple users to access the same books. Since books are
     universally common the users can share the books and authors tables. This reduces redundancy.
   - The users books information is stored in the library table along with details about the books availability by using the book_id and user_id.
   - I have created several unique key pairs so that the information does not overlap and access becomes easier.
   - Some of it may seem like premature optimisation, but the present structure allows me to add more features over time and makes the app more scaleable.

7. Lastly I will talk a little about the way the app looks. I loved being able to personalise the pages using css and bootstrap, getting a beautiful background and colourful tables.
```

Overall im really happy with my project and had fun making it. I really got to use all that I've learned. I found it easier to look things up and undeerstand cryptic answers that looked like gibberish during the first 3 weeks. The idea of programming no longer seems so daunting to me. This course has taught me a lot and i'm excited to keep learning. I have already signed up for the Web-Programming

course that im looking forward to beginning next.

