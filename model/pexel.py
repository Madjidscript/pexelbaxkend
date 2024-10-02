from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    years = db.Column(db.String(128), nullable=False)
    month = db.Column(db.String(128), nullable=False)
    day = db.Column(db.String(128), nullable=False)
    genre = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
