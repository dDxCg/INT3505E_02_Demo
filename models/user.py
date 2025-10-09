from db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # simple role system
    role = db.Column(db.String(50), default="user")  
    # options: "user", "admin"

    # 1 user -> many borrow records
    borrows = db.relationship("Borrow", back_populates="user", cascade="all, delete-orphan")
