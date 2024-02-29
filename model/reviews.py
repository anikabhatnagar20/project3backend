""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class BookReview(db.Model):
    __tablename__ = 'book_reviews'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), unique=False, nullable=False)
    _review = db.Column(db.String(255), unique=False, nullable=False)
    _rating = db.Column(db.Integer, unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, title, review, rating):
        self._title = title    # variables with self prefix become part of the object, 
        self._review = review
        self._rating = rating

    # a name getter method, extracts name from object
    @property
    def title(self):
        return self._title
    # a setter function, allows name to be updated after initial object creation
    @title.setter
    def title(self, title):
        self._title = title
    
    # a getter method, extracts email from object
    @property
    def review(self):
        return self._review
    
    # a setter function, allows name to be updated after initial object creation
    @review.setter
    def review(self, review):
        self._review = review

     # a getter method, extracts email from object
    @property
    def rating(self):
        return self._rating
    
    # a setter function, allows name to be updated after initial object creation
    @rating.setter
    def rating(self, rating):
        self._rating = rating    
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            print("error")
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "title": self.title,
            "review": self.review,
            "rating": self.rating
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, title="", review="", rating=""):
        """only updates values with length"""
        if len(title) > 0:
            self.title = title
        if len(review) > 0:
            self.review = review
        if len(rating) > 0:
            self.rating=rating
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

# Builds working data for testing
def initBookReviews():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        b1 = BookReview(title='The Great Gatsby', review='A classic piece', rating='5')
        b2 = BookReview(title='Harry Potter', review='A good read', rating='4')
        b3 = BookReview(title='Animal Farm', review='A classic piece', rating='5')
        b4 = BookReview(title='F451', review='dystopian story.', rating='4')
        BookReviews = [b1, b2, b3, b4]

        """Builds sample user/note(s) data"""
        for review in BookReviews:
            try:
                review.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate title, or error: {review.title}")
