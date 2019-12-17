"""
    disclaimer / attribution: 
    this code is an adaptation of 
    https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/03-Forms-and-Validation/forms.py
    Courtesy: Corey Schafer
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from mars_planet_library.settings import SETTINGS


"""
about "class RegistrationForm(FlaskForm):" implementation 
Currently, in order to make the website easy to use, the email field has been implemented as a stringField. 
Therefore it will accept any string, even if it is an empty string or if it is not an email
another possible implentation could be:
    email = StringField('Email', validators=[DataRequired(), Email()])
"""
class RegistrationForm(FlaskForm):
    username = StringField(SETTINGS.get("FORMS").get("USERNAME"), validators=[DataRequired(), Length(min=2, max=50)])   
    email = StringField(SETTINGS.get("FORMS").get("EMAIL"))
    password = PasswordField(SETTINGS.get("FORMS").get("PASSWORD"), validators=[DataRequired()])
    confirm_password = PasswordField(SETTINGS.get("FORMS").get("CONFIRM_PASSWORD"), validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(SETTINGS.get("FORMS").get("SIGN_UP"))


class LoginForm(FlaskForm):
    username = StringField(SETTINGS.get("FORMS").get("USERNAME"), validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField(SETTINGS.get("FORMS").get("PASSWORD"), validators=[DataRequired()])
    remember = BooleanField(SETTINGS.get("FORMS").get("REMMEMBER_ME"))
    submit = SubmitField(SETTINGS.get("FORMS").get("LOGIN"))


class SearchForm(FlaskForm):
    isbn = StringField(SETTINGS.get("FORMS").get("ISBN"), validators=[Length(min=0, max=15)])
    author_name = StringField(SETTINGS.get("FORMS").get("AUTHOR_NAME"), validators=[Length(min=0, max=50)])
    title = StringField(SETTINGS.get("FORMS").get("BOOK_TITLE"), validators=[Length(min=0, max=100)])
    submit = SubmitField(SETTINGS.get("FORMS").get("SEARCH")) 


class ReviewForm(FlaskForm):
    rating = RadioField("rating", choices = [("1","1"),("2","2"),("3","3"),("4","4"),("5","5")], default = "5")
    review = TextAreaField(SETTINGS.get("FORMS").get("REVIEW_INVITE"))
    submit = SubmitField(SETTINGS.get("FORMS").get("SUBMIT_REVIEW")) 


class BooksImport(FlaskForm):
    books_to_import = FileField(SETTINGS.get("FORMS").get("IMPORT_BOOKS"), validators=[FileAllowed(["csv"])])
    submit = SubmitField(SETTINGS.get("FORMS").get("IMPORT_CSV_FILE"))
    
    