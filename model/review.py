from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.review import Review

review_api = Blueprint('review_api', __name__,
                   url_prefix='/api/reviews')
# Model definition for book reviews
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(review_api)

import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
from model.review import BookReview

review_api = Blueprint('review_api', __name__, url_prefix='/api/reviews')
api = Api(review_api)

class ReviewAPI:
    class CRUD(Resource):
        @token_required
        def post(self, current_user):  # Create method for book review
            body = request.get_json()

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

            # Attempt to add book review to database
            try:
                book_review.create()
                return jsonify(book_review.read()), 201
            except Exception as e:
                return {'message': f'Error adding review: {str(e)}'}, 500

        @token_required
        def get(self, current_user):  # Read Method for all book reviews
            reviews = BookReview.query.all()
            json_ready = [review.read() for review in reviews]
            return jsonify(json_ready)

api.add_resource(ReviewAPI.CRUD, '/')

