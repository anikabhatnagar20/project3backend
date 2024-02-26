from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

# Model definition for book reviews
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
from model.review import BookReview

review_api = Blueprint('review_api', __name__, url_prefix='/api/book_reviews')
api = Api(review_api)

class ReviewAPI:
    class _CRUD(Resource):
        def post(self):  # Create method for book review
            body = request.get_json()
            print("hi")
            # Validate title
            title = body.get('title')
            if title is None or len(title) < 2:
                return {'message': 'Title is missing, or is less than 2 characters'}, 400

            # Validate review
            review = body.get('review')
            if review is None or len(review) < 10:
                return {'message': 'Review is missing, or is less than 10 characters'}, 400

            # Validate rating
            rating = body.get('rating')
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                return {'message': 'Rating must be an integer between 1 and 5'}, 400

            # Create book review object
            book_review = BookReview(title=title, review=review, rating=rating)
            
            book_review.create()
            # Attempt to add book review to database
    
            return jsonify(book_review.read())
            return {'message': f'Error adding review: {str()}'}, 500
        @token_required()
        def get(self, _):  # Read Method for all book reviews
            reviews = BookReview.query.all()
            json_ready = [review.read() for review in reviews]
            return jsonify(json_ready)

    api.add_resource(_CRUD, '/')
