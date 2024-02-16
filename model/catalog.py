from flask import Flask, request, render_template_string

app = Flask(__name__)

# Sample catalog of books
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "1984", "author": "George Orwell"},
    # Add more books as needed
]

@app.route('/')
def home():
    return render_template_string('''
        <h1>Book Catalog</h1>
        <form action="/search" method="get">
            <input type="text" name="query" placeholder="Search books by title...">
            <input type="submit" value="Search">
        </form>
        <ul>
            {% for book in books %}
                <li>{{ book.title }} by {{ book.author }}</li>
            {% endfor %}
        </ul>
    ''', books=books)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    filtered_books = [book for book in books if query in book['title'].lower()]
    return render_template_string('''
        <h1>Search Results</h1>
        <form action="/search" method="get">
            <input type="text" name="query" placeholder="Search books by title...">
            <input type="submit" value="Search">
        </form>
        <ul>
            {% for book in filtered_books %}
                <li>{{ book.title }} by {{ book.author }}</li>
            {% endfor %}
        </ul>
        <a href="/">Back to catalog</a>
    ''', filtered_books=filtered_books)

if __name__ == '__main__':
    app.run(debug=True)