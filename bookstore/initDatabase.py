import sqlite3
import pymongo

from sqlalchemy_utils import drop_database, create_database
from sqlalchemy.orm import sessionmaker, session, declarative_base
from sqlalchemy import Column, String, create_engine, Integer, Text, LargeBinary

drop_database('postgresql://postgres:wennitao@localhost/bookstore')

create_database('postgresql://postgres:wennitao@localhost/bookstore')

conn = sqlite3.connect('fe/data/book.db')
cur = conn.cursor()
cur.execute("SELECT * FROM book")
rows = cur.fetchall()
cur.close()
conn.close()

# client = pymongo.MongoClient ('localhost', 27017)
# client.drop_database("bookstore")
# db = client['bookstore']
# books = db['book']

from be.model.database import getDatabaseSession, getDatabaseBase, init_database
from fe.access.book import BookTable

init_database()

for row in rows:
    book = {
        'id': row[0],
        'title': row[1],
        'author': row[2],
        'publisher': row[3],
        'original_title': row[4],
        'translator': row[5],
        'pub_year': row[6],
        'pages': row[7],
        'price': row[8],
        'currency_unit': row[9],
        'binding': row[10],
        'isbn': row[11],
        'author_intro': row[12],
        'book_intro': row[13],
        'content': row[14],
        'tags': row[15],
        'picture': row[16]
    }
    new_book = BookTable (
        id = book['id'],
        title = book['title'],
        author = book['author'],
        publisher = book['publisher'],
        original_title = book['original_title'],
        translator = book['translator'],
        pub_year = book['pub_year'],
        pages = book['pages'],
        price = book['price'],
        currency_unit = book['currency_unit'],
        binding = book['binding'],
        isbn = book['isbn'],
        author_intro = book['author_intro'],
        book_intro = book['book_intro'],
        content = book['content'],
        tags = book['tags'],
        picture = book['picture']
    )
    session = getDatabaseSession()
    session.add (new_book)
    session.commit()

session.close()
# client.close()