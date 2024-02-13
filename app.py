# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

# Create the initial database
db.create_all()

# --- New Code for Review System ---

# HTML content for the review box
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Include your styles here */
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 50px;
        }
        input, textarea {
            margin-bottom: 10px;
        }
        #reviewForm {
            display: inline-block;
            text-align: left;
        }
    </style>
</head>
<body>
    <form id="reviewForm">
        <label for="bookTitle">Book Title:</label>
        <input type="text" id="bookTitle" name="bookTitle" required><br>

        <label for="text">Review:</label>
        <textarea id="text" name="text" rows="4" required></textarea><br>

        <label for="rating">Rating (1-5):</label>
        <input type="number" id="rating" name="rating" min="1" max="5" required><br>

        <button type="button" onclick="submitReview()">Submit Review</button>
    </form>

    <script>
        // JavaScript for Fetch
        function submitReview() {
            const bookTitle = document.getElementById('bookTitle').value;
            const text = document.getElementById('text').value;
            const rating = document.getElementById('rating').value;

            fetch('http://127.0.0.1:5000/api/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ bookTitle, text, rating }),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);  // Display success or failure message
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
'''

# Endpoint to display the review box
@app.route('/review-box', methods=['GET'])
def review_box():
    return html_content

# --- End of New Code ---

# Endpoint to handle review submissions
@app.route('/api/reviews', methods=['POST'])
def submit_review():
    # Rest of the code remains unchanged
    # ...

# Endpoint to retrieve all reviews
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    # Rest of the code remains unchanged
    # ...

if __name__ == "__main__":
    app.run(debug=True)
