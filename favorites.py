# favorites.py
import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from models import FavoriteRead  # Import the FavoriteRead model

favorites_api = Blueprint('favorites_api', __name__, url_prefix='/api/favorites')
api = Api(favorites_api)

class FavoritesAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            title = body.get('title')

            if title:
                favorite = FavoriteRead(title=title)
                favorite.save()

                return jsonify({"message": "Favorite added successfully"}), 201
            else:
                return jsonify({"error": "Title is required"}), 400

        def get(self):
            favorites = FavoriteRead.query.all()
            json_ready = [favorite.serialize() for favorite in favorites]
            return jsonify(json_ready)

    api.add_resource(_CRUD, '/')
