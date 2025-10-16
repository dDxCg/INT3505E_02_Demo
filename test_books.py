from app import create_app
from db import db
from models.book import Book
from models.copy import Copy

app = create_app()

with app.app_context():
    # for book_id in range(2, 6):
    #     db.session.add(Copy(book_id=book_id, status="available"))
    # db.session.commit()

    books = Book.query.options(db.joinedload(Book.copies)).limit(5).all()
    for b in books:
        print(b.id, b.title, [c.status for c in b.copies])

    for c in Copy.query.all():
        print(c.id, c.book_id, c.status)