from db import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=True)

    # 1 book -> many copies
    copies = db.relationship("Copy", back_populates="book", cascade="all, delete-orphan")
