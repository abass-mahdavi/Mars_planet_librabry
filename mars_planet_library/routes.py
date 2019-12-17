import os
from flask import Flask, render_template, url_for, flash, redirect, make_response, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from mars_planet_library import app, settings, forms, database_requests


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", SETTINGS=settings.SETTINGS)


@app.route("/about")
def about():
    return render_template("about.html", SETTINGS=settings.SETTINGS)


@app.route("/register", methods=["GET", "POST"])
def register():
    registration_form = forms.RegistrationForm()
    if registration_form.validate_on_submit():
        try:
            user = database_requests.resister_user(
                registration_form.username.data,
                registration_form.email.data,
                registration_form.password.data
            )
        except:  
            flash(f'{settings.SETTINGS.get("CONSTANTS").get("REGISTRATION_FAILED")}', "danger")
            return redirect(url_for("home")) 
        if user is not None:
            flash(f'{settings.SETTINGS.get("CONSTANTS").get("FLASH_MESSAGE_ACCOUNT_CREATED_FOR")} \
                {user.name}!', "success")
            return redirect(url_for("home"))
        else:
            flash(f'{registration_form.username.data} \
                {settings.SETTINGS.get("CONSTANTS").get("IS_ALREADY_REGISTERED")}', "danger")
            return redirect(url_for("register"))          
    return render_template(
        "register.html", 
        form=registration_form, 
        SETTINGS=settings.SETTINGS)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        user = database_requests.check_user(login_form.username.data, login_form.password.data)        
        if user:
            login_user(user, remember=login_form.remember.data)
            flash(f'{settings.SETTINGS.get("CONSTANTS").get("FLASH_MESSAGE_SUCCESSFUL_LOGIN")}', "success")
            return redirect(url_for("home"))
        else:
            flash(f'{settings.SETTINGS.get("CONSTANTS").get("FLASH_MESSAGE_LOGIN_FAILURE")}', "danger")
            return redirect(url_for("login"))
    return render_template(
        "login.html", 
        form=login_form, 
        SETTINGS=settings.SETTINGS)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():    
    search_form = forms.SearchForm()
    if search_form.validate_on_submit():
        if search_form.title.data or search_form.author_name.data or search_form.isbn.data:
            books = database_requests.books_search_result(
                search_form.isbn.data, search_form.author_name.data, search_form.title.data,"")
            book_search_result_message = settings.book_search_result_message(len(books))
            return render_template(
                "search_result.html", 
                books=books, 
                message = book_search_result_message, 
                SETTINGS=settings.SETTINGS)
        else:
            flash(f'{settings.SETTINGS.get("CONSTANTS").get("ONE_FIELD_AT_LEAST_REQUIRED")}', "danger")
            return redirect(url_for("search"))
    return render_template(
        "search.html", 
        form=search_form, 
        SETTINGS=settings.SETTINGS)


@app.route("/book/<book_id>", methods=["GET", "POST"])
@login_required
def book(book_id):
    review_form = forms.ReviewForm()
    book = database_requests.book(book_id) 
    if book:
        user_id = current_user.id
        #sends true if the current user has already rated the featured book
        already_rated = database_requests.book_already_reviewd_by_user(book_id,user_id) 
        # gets the rating and review of current user on submission
        if review_form.validate_on_submit(): 
            try:
                rating = int(review_form.rating.data)
                review = review_form.review.data
                database_requests.rate_and_review_book(book_id, current_user.id, rating, review)
                flash(f'{settings.SETTINGS.get("CONSTANTS").get("FLASH_MESSAGE_SUCCESSFUL_REVIEW")}', "success")
                return redirect("/book/{}".format(book_id))
            except:
                flash(f'{settings.SETTINGS.get("CONSTANTS").get("FLASH_MESSAGE_REVIEW_FAILURE")}', "danger")
                return redirect(url_for("home"))
        return render_template("book.html", 
                                book = book,
                                already_rated = already_rated, # True or False
                                form = review_form,
                                SETTINGS=settings.SETTINGS)
    else:
        abort(404, description="Resource not found")


#api routes 404
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


#MPL api
@app.route("/api/<string:isbn>")
def api(isbn):
    api = database_requests.api(isbn)
    if api:
        api = jsonify(api)
        return make_response(api, 200)
    else:
        abort(404, description="Resource not found")


"""
warning, do not use this route in production, it can genrate bugs...
"""
@app.route("/import_books", methods=["GET", "POST"])
@login_required
def import_books():      
    if current_user.username != "MPL_admin":     #pw user MPL_admin: mpt-pub "MPL_admin" b6 hint 988        
        return redirect(url_for('home'))
    else:
        import_books_form = forms.BooksImport()
        if import_books_form.validate_on_submit():
            if database_requests.books_file_database_import(import_books_form.books_to_import.data):
                return redirect(url_for('home'))   
        return render_template(
            "import_books.html", 
            form = import_books_form, 
            SETTINGS=settings.SETTINGS)


    
