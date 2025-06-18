from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, get_db
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


BOOKS = []


@app.get("/")
def get_book(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


# query parameters, id
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
# return {"item_id": item_id, "q": q}


@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Book()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()
    return book


@app.put("/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    book_model = db.query(models.Book).filter(models.Book.id == book.id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404, detail=f"Book with id {book_id} does not exist"
        )

    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()
    return book


@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404, detail=f"Book with id {book_id} does not exist"
        )
    
    db.delete(book_model)
    db.commit()
    return 'deleted successfully'
