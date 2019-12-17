#this is a standalone module to import csv book file (as requested) but 
#it is not used for the project 
#books are imported trues routes.py def import_books(): 
#which uses database_requests.py def books_file_database_import(csv_file_as_FileForm_data):

import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	f = open("books.csv")
	reader = csv.reader(f)
	next(f) #ignore first line of csv
	for isbn, title, author, year in reader:
		# Make sure isbn is unique.
		if db.execute("SELECT * FROM books WHERE isbn = :isbn", 
				{"isbn": isbn}).rowcount != 0:
			next(f) # book is already in database move to next book
		else:
			# check if author is already in authors database
			if db.execute("SELECT id FROM authors WHERE name=:name",
					{"name":author}).rowcount != 0:
				# request author's author_id
				author_id = db.execute(
					"SELECT id FROM authors WHERE name=:name",
					{"name":author}).fetchone()[0]
			else:  
				# create author in authors database
				db.execute("INSERT INTO authors (name) VALUES (:name)",
					{"name":author})
				# request the newly inserted author author_id
				author_id = db.execute(
					"SELECT id FROM authors WHERE name=:name",
					{"name":author}).fetchone()[0]
			# insert book in database
			db.execute("INSERT INTO books \
				(isbn, title, author_id, year) \
				VALUES (:isbn, :title, :author_id, :year)", 
				{"isbn":isbn, "title":title, 
				"author_id":author_id, "year":year})
	db.commit()


if __name__ == "__main__":
	main()

