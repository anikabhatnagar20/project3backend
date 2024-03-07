import threading

# import "packages" from flask
from flask import Flask, render_template, request  # import render_template from "public" flask libraries
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import the CORS module
from models import db, FavoriteRead  # Import the models
from favorites import favorites_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///favorites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# register URIs
app.register_blueprint(favorites_api)  # Assuming favorites_api is defined in the favorites module
# Add the necessary imports for joke_api, covid_api, user_api, player_api, and app_projects

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:8999', 'http://127.0.0.1:8999', 'https://nighthawkcoders.github.io', 'http://10.0.0.36:8999']:
        CORS(app, resources={r"/*": {"origins": allowed_origin}})

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()

# Placeholder for the initUsers function
def initUsers():
    pass

# Placeholder for the initPlayers function
def initPlayers():
    pass

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8999")
