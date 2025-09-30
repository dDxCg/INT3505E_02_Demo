from db import db
from datetime import datetime

class Borrow(db.Model):
    __tablename__ = "borrows"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    copy_id = db.Column(db.Integer, db.ForeignKey("copies.id"), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)

    # relationships
    user = db.relationship("User", back_populates="borrows")
    copy = db.relationship("Copy", back_populates="borrows")
