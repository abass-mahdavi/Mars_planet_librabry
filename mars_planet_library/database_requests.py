import requests, csv
from flask_login import UserMixin
from io import StringIO
from mars_planet_library import login_manager, db, bcrypt, settings

"""
needed for login_manager and current_user
"""
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


"""
needed for login_mamgement and current_user
"""
class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


"""
 returns an instance of User class
 if the user_id is not in the database, it returns None
 otherwise, it sets the id, name, email and password to those in database users table
"""
def get_user_by_id(user_id):
    user = db.execute("SELECT * FROM users WHERE id = :id", {"id": user_id}).fetchone()
    if user is None:
        return None
    else:
        user = dict(user)
        return User(user.get("id"), user.get("name"), user.get("email"), user.get("password_hash"))


"""
 returns an instance of User class
 if the name is not in the database, it returns None
 otherwise, it sets the id, name, email and password to those in database users table
"""
def get_user_by_name(name):
    user = db.execute("SELECT * FROM users WHERE name = :name", {"name": name}).fetchone()
    if user is None:
        return None
    else:
        user = dict(user)
        return User(user.get("id"), user.get("name"), user.get("email"), user.get("password_hash"))


"""
checks if there is a user in the users table with name 0 name and a matching password
"""
def check_user(name, password): 
    user = get_user_by_name(name)
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    else:
        return None


"""
registers a new user after having checked that there is not already a registered user with the same username
"""
def resister_user(name,email,password):
    if get_user_by_name(name):
        return None  # username already registered
    else:
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        try:
            db.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (:name, :email, :password_hash)",
                {
                    "name": name,
                    "email": email,
                    "password_hash": password_hash,
                },
            )
            db.commit()
            return get_user_by_name(name)  # returns the inserted user with it's databse id and hashed_password
        except:
            raise  # rethrows the exeption if raised


"""
def books_search_result(isbn, author_name, title, book_id):
returns all the books that (partly) match all provided search parameters as list
for exemple books_search_result("", "asim", "rob", "") would return something like:
    [
    {'id': 25004, 'year': 1950, 'isbn': '0553803700', 'title': 'I, Robot', 'author_name': 'Isaac Asimov'}, 
    {'id': 28205, 'year': 1985, 'isbn': '0586062009', 'title': 'Robots and Empire', 'author_name': 'Isaac Asimov'}, 
    {'id': 28665, 'year': 1983, 'isbn': '0553299492', 'title': 'The Robots of Dawn', 'author_name': 'Isaac Asimov'}, 
    {'id': 29496, 'year': 1982, 'isbn': '0586057242', 'title': 'The Complete Robot', 'author_name': 'Isaac Asimov'}
    ]
similarly books_search_result("", "charles", "the", "") would return something like:
    [
    {'id': 25659, 'year': 2013, 'isbn': '1402284314', 'title': 'The Paris Architect', 'author_name': 'Charles Belfoure'}, 
    {'id': 29247, 'year': 2011, 'isbn': '1400069289', 'title': 'The Power of Habit', 'author_name': 'Charles Duhigg'}, 
    {'id': 28910, 'year': 2004, 'isbn': '0441013651', 'title': 'The Atrocity Archives', 'author_name': 'Charles Stross'}
    ]
"""
def books_search_result(isbn, author_name, title, book_id):
    books_list = []
    previous = False
    where_isbn = ""
    where_name = ""
    where_title = ""
    where_book_id = ""
    if isbn or author_name or title or id:
        if isbn:
            isbn = "%" + isbn.lower() + "%"
            where_isbn += "LOWER(isbn) LIKE :isbn"
            previous = True
        if author_name:
            author_name = "%" + author_name.lower() + "%"
            if previous:
                where_name += " AND"
            where_name += " LOWER(name) LIKE :name"
            previous = True
        if title:
            title = "%" + title.lower() + "%"
            if previous:
                where_title += " AND"
            where_title += " LOWER(title) LIKE :title"
            previous = True
        if book_id:
            if previous:
                where_book_id += " AND"
            where_book_id += " books.id = :book_id"        
        query_string =   """SELECT books.id, year, isbn, name, title FROM books JOIN authors ON books.author_id = authors.id 
                            WHERE {}{}{}{} ORDER BY name""".format(where_isbn, where_name, where_title, where_book_id)
        books = db.execute(query_string, {"isbn": isbn, "name": author_name, "title": title, "book_id":book_id}).fetchall()
        for book in books:
            book = dict(book)
            book["author_name"]=book.pop("name") #change name key label to author_name key label
            books_list.append(book)
    return books_list


"""
contrary to books_search_result(isbn, author_name, title, book_id): 
this function will not accept part of the isbn, it needs the exact isbn 
if there is a relevant book, it returns the book details (most important for our purpose. its id)
otherwise it returns None
"""
def book_details_by_isbn(isbn):
    if db.execute("SELECT * FROM books WHERE isbn =:isbn",{"isbn" : isbn}).fetchone():
        return books_search_result(isbn, "", "","")
    else:
        return None


"""
def book(book_id):
returns a detailed set of information regarding the featured book as a dictionnary 
for example book("28172") will return somethin like:
    {
    'book_details': 
        {
        'id': 28172, 
        'year': 2007, 
        'isbn': '0061161640', 
        'title': 'Making Money', 
        'author_name': 
        'Terry Pratchett'
        }, 
    'goodreads_datas': 
        {'id': 
        116296, 
        'isbn': '0061161640', 
        'isbn13': '9780061161643', 
        'ratings_count': 46491, 
        'reviews_count': 68571, 
        'text_reviews_count': 1340, 
        'work_ratings_count': 54118, 
        'work_reviews_count': 80926, 
        'work_text_reviews_count': 1771, 
        'average_rating': '4.24'
        }, 
    'reviews': 
        [
        ('john', 5, 'made lots of money'), 
        ('jane', 5, 'I made tons of money thanks to this book'), 
        ('john doe', 5, 'how to become rich'), 
        ('superman', 5, 'awsome')
        ], 
    'number_of_reviews': 9, 
    'average_review_score': '4.56'
    }
"""
def book(book_id):
    book = {}
    book_details = books_search_result("", "", "", book_id)
    if book_details:  
        book_details = book_details[0]
        book[settings.SETTINGS.get("CONSTANTS").get("BOOK_DATAS")] = book_details
        isbn = book_details.get("isbn")
        book[settings.SETTINGS.get("CONSTANTS").get("GOODREADS_DATAS")] = goodreads_datas(isbn)
        reviews = book_reviews(book_id)
        book[settings.SETTINGS.get("CONSTANTS").get("REVIEWS")] = reviews
        book[settings.SETTINGS.get("CONSTANTS").get("NUMBER_OF_REVIEWS")] = len(reviews)
        average_score = average_review_score(book_id)[0]
        if average_score:        
            average_score = '%.2f' % average_score #issue the average review as a 2 decimals string (readable format)
        else:
            average_score = settings.SETTINGS.get("CONSTANTS").get("NOT_RELEVANT")
        book[settings.SETTINGS.get("CONSTANTS").get("AVERAGE_REVIEW_SCORE")] = average_score
    return book 


"""
def api(isbn):
returns a dictionary containning part of the informations returned by previous function def book(book_id):
for example api("0061161640") will return something like:
    {
    "author": "Terry Pratchett", 
    "average_score": "4.56", 
    "review_count": 9, 
    "title": "Making Money", 
    "year": 2007
    }
"""
def api(isbn):
    api = {}
    book_by_isbn = book_details_by_isbn(isbn)
    if book_by_isbn:
        id = book_by_isbn[0].get("id")
        book_by_id = book(id)
        api[settings.SETTINGS.get("API_FIELDS").get("TITLE")] =  \
            book_by_id.get(settings.SETTINGS.get("CONSTANTS").get("BOOK_DATAS")).get("title")
        api[settings.SETTINGS.get("API_FIELDS").get("AUTHOR")] =  \
            book_by_id.get(settings.SETTINGS.get("CONSTANTS").get("BOOK_DATAS")).get("author_name")
        api[settings.SETTINGS.get("API_FIELDS").get("YEAR")] =  \
            book_by_id.get(settings.SETTINGS.get("CONSTANTS").get("BOOK_DATAS")).get("year")
        api[settings.SETTINGS.get("API_FIELDS").get("REVIEW_COUNT")] =  \
            book_by_id.get(settings.SETTINGS.get("CONSTANTS").get("NUMBER_OF_REVIEWS"))
        api[settings.SETTINGS.get("API_FIELDS").get("AVERAGE_COUNT")] =  \
            book_by_id.get(settings.SETTINGS.get("CONSTANTS").get("AVERAGE_REVIEW_SCORE"))
        return api
    else: 
        return None



"""
def goodreads_datas(isbn): is a helper fountion to get goodreads website api
goodreads_datas("0061161640") will return something like
    {
    'id': 116296, 
    'isbn': '0061161640', 
    'isbn13': '9780061161643', 
    'ratings_count': 46491, 
    'reviews_count': 68571, 
    'text_reviews_count': 1340, 
    'work_ratings_count': 54118, 
    'work_reviews_count': 80926, 
    'work_text_reviews_count': 1771, 
    'average_rating': '4.24'
    }
"""
def goodreads_datas(isbn):
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params =  \
        {"key": settings.SECURITY_SETTINGS.get("GOODREADS_KEY"), "isbns": isbn})
	if res.status_code == 200:
		return res.json().get("books")[0]
	else:
		return {    'work_reviews_count': settings.SETTINGS.get("CONSTANTS").get("NOT_RELEVANT"), 
                    'average_rating': settings.SETTINGS.get("CONSTANTS").get("NOT_RELEVANT") }



"""
def book_reviews(book_id): is a helper function, returns all the reviews related to the book with id book_id
def book_reviews("28172") will return something like:
    [
    ('ii', 5, 'made lots of money'), 
    ('pp', 5, 'I made tons of money thanks to this book'), 
    ('PP', 5, 'how to become rich'), 
    ('gg', 5, 'awsome')
    ]
"""
def book_reviews(book_id):
    query_string = "SELECT name, rating, review FROM reviews JOIN users ON reviews.user_id = users.id WHERE book_id =:book_id"
    return db.execute(query_string,{"book_id" : book_id}).fetchall()


"""
simply returns the average review rating scores
"""
def average_review_score(book_id):
    query_string = "SELECT AVG(rating) FROM reviews WHERE book_id =:book_id"
    return db.execute(query_string,{"book_id" : book_id}).fetchone()


"""
verifies if the current_user has already rated the featured book or not
"""
def book_already_reviewd_by_user(book_id,user_id):
    query_string = "SELECT * FROM reviews WHERE book_id =:book_id AND user_id =:user_id"
    if db.execute(query_string,{"book_id" : book_id, "user_id" :user_id}).rowcount != 0:
        return True
    else:
        return False


"""
inserts rating and review in database
"""
def rate_and_review_book(book_id, user_id, rating, review):
    if not book_already_reviewd_by_user(book_id,user_id):
        try:
            db.execute(
                    "INSERT INTO reviews (book_id, user_id, rating, review ) VALUES (:book_id, :user_id, :rating, :review)",
                        {
                            "book_id":book_id, 
                            "user_id": user_id, 
                            "rating": rating, 
                            "review": review
                        },
                    )            
            db.commit()
            return True
        except:
            raise  # rethrows the exeption if raised
    else:
        return False


"""
WARNING: DO NOT USE THIS FUNCTION YET... IT IS UNDER DEVELOPPMENT
def books_file_database_import(csv_file_as_FileForm_data):
Warning, it is a beta function ... it works well on localhost but bugs in production for large lists
It is aimed to allow user to imports a book catalog in the database
Currently, it is recommendaed to NOT use this function, but instead use the Import module

possible solutions:
we also could have saved the "csv_file_as_FileForm_data" to the local drive and then open the saved file
a possible code would be :

        f = csv_file_as_FileForm_data
        #filename = secure_filename(f.filename)
        f.save(os.path.join('import', 'tempoFile.csv')) #will save under./import/tempoFile.csv

or... add some try/except 
"""
def books_file_database_import(csv_file_as_FileForm_data):
    f = StringIO(csv_file_as_FileForm_data.stream.read().decode('utf-8'))
    reader = csv.reader(f, delimiter = ',')
    next(f) #ignore first line of csv
    for isbn, title, author, year in reader:
        # Make sure isbn is unique.
        if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount != 0:
            next(f) # book is already in database move to next book
        else:
            # check if author is already in authors database
            if db.execute("SELECT id FROM authors WHERE name=:name", {"name":author}).rowcount != 0:
            # request author's author_id
                author_id = db.execute("SELECT id FROM authors WHERE name=:name",{"name":author}).fetchone()[0]
            else:
                try:
                    # create author in authors database
                    db.execute("INSERT INTO authors (name) VALUES (:name)",{"name":author})
                    # request the newly inserted author author_id
                    author_id = db.execute(
                    "SELECT id FROM authors WHERE name=:name", {"name":author}).fetchone()[0]
                    # insert book in database
                    db.execute(
                        "INSERT INTO books (isbn, title, author_id, year) VALUES (:isbn, :title, :author_id, :year)", 
                        {
                            "isbn":isbn, 
                            "title":title, 
                            "author_id":author_id, 
                            "year":year
                        })                    
                except:
                    raise  # rethrows the exeption if raised
    try:   
        db.commit()
        return True
    except:
        raise  # rethrows the exeption if raised
    return False

