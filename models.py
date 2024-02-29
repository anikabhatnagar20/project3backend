# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        return {
            'id': self.id,
            'name': self.name,
            'uid': self.uid,
            'dob': str(self.dob) if self.dob else None
        }

class FavoriteRead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('favorites', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'created_at': str(self.created_at)
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
