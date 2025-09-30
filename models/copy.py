from db import db

class Copy(db.Model):
    __tablename__ = "copies"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    status = db.Column(db.String(50), default="available")  
    # available / borrowed

    # link back to book
    book = db.relationship("Book", back_populates="copies")

    # 1 copy -> many borrow records
    borrows = db.relationship("Borrow", back_populates="copy", cascade="all, delete-orphan")
