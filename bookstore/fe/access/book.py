import os
from typing import List
# import sqlite3 as sqlite
# import pymongo
# from be.model.collection import Collection
from be.model.database import getDatabaseSession, getDatabaseBase
from sqlalchemy import Column, String, create_engine, Integer, Text, LargeBinary
import random
import base64
import simplejson as json

Base = getDatabaseBase()

class BookTable(Base):
    __tablename__ = "book"

    id = Column(Text, primary_key=True, unique=True, nullable=False)
    title = Column(Text)
    author = Column(Text)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    price = Column(Integer)
    currency_unit = Column(Text)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    picture = Column(LargeBinary)

    def to_dict (self, picStr):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "original_title": self.original_title,
            "translator": self.translator,
            "pub_year": self.pub_year,
            "pages": self.pages,
            "price": self.price,
            "currency_unit": self.currency_unit,
            "binding": self.binding,
            "isbn": self.isbn,
            "author_intro": self.author_intro,
            "book_intro": self.book_intro,
            "content": self.content,
            "tags": self.tags,
            "picture": picStr,
        }

class Book:
    id: str
    title: str
    author: str
    publisher: str
    original_title: str
    translator: str
    pub_year: str
    pages: int
    price: int
    currency_unit: str
    binding: str
    isbn: str
    author_intro: str
    book_intro: str
    content: str
    tags: List[str]
    pictures: List[bytes]

    def __init__(self):
        self.tags = []
        self.pictures = []


class BookDB:
    def __init__(self, large: bool = False):
        # parent_path = os.path.dirname(os.path.dirname(__file__))
        # self.db_s = os.path.join(parent_path, "data/book.db")
        # self.db_l = os.path.join(parent_path, "data/book_lx.db")
        # if large:
        #     self.book_db = self.db_l
        # else:
        #     self.book_db = self.db_s
        # self.bookCollection = Collection ("book").collection
        pass

    def get_book_count(self):
        # conn = sqlite.connect(self.book_db)
        # cursor = conn.execute(
        #     "SELECT count(id) FROM book")
        # row = cursor.fetchone()
        session = getDatabaseSession()
        return len (session.query(BookTable).all())
        # return self.bookCollection.count_documents({})

    def get_book_info(self, start, size) -> List[Book]:
        books = []
        # conn = sqlite.connect(self.book_db)
        # cursor = conn.execute(
        #     "SELECT id, title, author, "
        #     "publisher, original_title, "
        #     "translator, pub_year, pages, "
        #     "price, currency_unit, binding, "
        #     "isbn, author_intro, book_intro, "
        #     "content, tags, picture FROM book ORDER BY id "
        #     "LIMIT ? OFFSET ?", (size, start))
        # result = self.bookCollection.find(
        #     {}, 
        #     {
        #         "_id": 0,
        #         "id": 1,
        #         "title": 1,
        #         "author": 1,
        #         "publisher": 1,
        #         "original_title": 1,
        #         "translator": 1,
        #         "pub_year": 1,
        #         "pages": 1,
        #         "price": 1,
        #         "currency_unit": 1,
        #         "binding": 1,
        #         "isbn": 1,
        #         "author_intro": 1,
        #         "book_intro": 1,
        #         "content": 1,
        #         "tags": 1,
        #         "picture": 1,
        #     }
        # ).sort("id", pymongo.ASCENDING).skip(start).limit(size)
        session = getDatabaseSession()
        result = session.query(BookTable).order_by(BookTable.id).offset(start).limit(size).all()
        for row in result:
            book = Book()
            book.id = row.id
            book.title = row.title
            book.author = row.author
            book.publisher = row.publisher
            book.original_title = row.original_title
            book.translator = row.translator
            book.pub_year = row.pub_year
            book.pages = row.pages
            book.price = row.price
            book.currency_unit = row.currency_unit
            book.binding = row.binding
            book.isbn = row.isbn
            book.author_intro = row.author_intro
            book.book_intro = row.book_intro
            book.content = row.content
            tags = row.tags
            picture = row.picture

            for tag in tags.split("\n"):
                if tag.strip() != "":
                    book.tags.append(tag)
            for i in range(0, random.randint(0, 9)):
                if picture is not None:
                    encode_str = base64.b64encode(picture).decode('utf-8')
                    book.pictures.append(encode_str)
            books.append(book)
            # print(tags.decode('utf-8'))

            # print(book.tags, len(book.picture))
            # print(book)
            # print(tags)

        return books


