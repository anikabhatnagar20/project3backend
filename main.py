# main.py
from flask import Flask, render_template, request, jsonify
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import the CORS module
from models import db, FavoriteRead  # Import the models
from favorites import favorites_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///favorites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)  # Initialize CORS for the entire app

# Create the SQLite database tables
with app.app_context():
    db.create_all()

# Register the blueprints
app.register_blueprint(favorites_api)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table/')
def table():
    return render_template("table.html")

@app.before_request
def before_request():
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:8999', 'http://127.0.0.1:8999', 'https://nighthawkcoders.github.io', 'http://10.0.0.36:8999']:
        CORS(app, resources={r"/*": {"origins": allowed_origin}})

custom_cli = AppGroup('custom', help='Custom commands')

def initFavorites():
    # Your initialization logic for favorites here
    pass

@custom_cli.command('generate_data')
def generate_data():
    initFavorites()

app.cli.add_command(custom_cli)

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8999")
