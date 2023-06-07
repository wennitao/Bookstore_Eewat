from sqlalchemy import Column, String, create_engine, Integer, Text, Date, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, session, declarative_base
import time

# from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

print ("database.py")

class Database:
    def __init__ (self):
        self.engine = create_engine("postgresql://postgres:wennitao@127.0.0.1:5432/bookstore",
            # echo=True,
            pool_size=8, 
            pool_recycle=60*30
        )
        self.DbSession = sessionmaker(bind=self.engine)
        self.session = self.DbSession()
        self.base = declarative_base()
    
    def getEngine (self):
        return self.engine

    def getSession (self):
        return self.session
    
    def getBase (self):
        return self.base

    def __del__ (self):
        self.session.close()

database_instance: Database = Database()
# database_instance: Database = None

def getDatabaseBase():
    global database_instance
    return database_instance.getBase()

def getDatabaseSession () -> session:
    global database_instance
    return database_instance.getSession()

Base = getDatabaseBase()

class User_store (Base):
    __tablename__ = "user_store"

    user_id = Column(Text, primary_key=True, nullable=False)
    store_id = Column(Text, primary_key=True, nullable=False)

class Store (Base):
    __tablename__ = "store"

    store_id = Column(Text, primary_key=True, nullable=False)
    book_id = Column(Text, primary_key=True, nullable=False)
    book_info = Column(Text, nullable=False)
    stock_level = Column(Integer, nullable=False)

class New_order (Base):
    __tablename__ = "new_order"

    order_id = Column(Text, primary_key=True, unique=True, nullable=False)
    user_id = Column(Text, nullable=False)
    store_id = Column(Text, nullable=False)
    order_time = Column(DateTime, nullable=False)
    total_price = Column(Integer, nullable=False)
    paid = Column(Boolean, nullable=False)
    cancelled = Column(Boolean, nullable=False)
    delivered = Column(Boolean, nullable=False)

class New_order_detail (Base):
    __tablename__ = "new_order_detail"

    order_id = Column(Text, primary_key=True, nullable=False)
    book_id = Column(Text, primary_key=True, nullable=False)
    count = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "book_id": self.book_id,
            "count": self.count,
            "price": self.price
        }

# class User(Base):
#     print ("init user")
#     __tablename__ = "user"

#     user_id = Column(String(50), primary_key=True, unique=True, nullable=False)
#     password = Column(String(50), nullable=False)
#     balance = Column (Integer, nullable=False)
#     token = Column (Text)
#     terminal = Column (Text)

def init_database():
    print ("init_database")
    global database_instance
    # database_instance = Database()
    engine = database_instance.getEngine()
    print ("creating tables")
    database_instance.getBase().metadata.create_all(engine)

def user_id_exist(user_id) -> bool:
    # user_collection = getDatabase()['user']
    # cursor = self.conn.execute("SELECT user_id FROM user WHERE user_id = ?;", (user_id,))
    # row = cursor.fetchone()
    # result = user_collection.find ({'user_id': user_id})
    # result_list = list (result)
    from be.model.user import User
    session = getDatabaseSession()
    result = session.query(User).filter(User.user_id == user_id).all()
    if len (result) == 0:
        return False
    else:
        return True
    
def book_id_exist(store_id, book_id):
    # cursor = self.conn.execute("SELECT book_id FROM store WHERE store_id = ? AND book_id = ?;", (store_id, book_id))
    # row = cursor.fetchone()
    # store_collection = getDatabase()['store']
    # result = store_collection.find ({'store_id': store_id, 'book_id': book_id})
    # result_list = list (result)
    session = getDatabaseSession()
    result = session.query(Store).filter(Store.store_id == store_id, Store.book_id == book_id).all()
    # print (result)
    if len (result) == 0:
        return False
    else:
        return True

def store_id_exist(store_id):
    # cursor = self.conn.execute("SELECT store_id FROM user_store WHERE store_id = ?;", (store_id,))
    # row = cursor.fetchone()
    # user_store_collection = getDatabase()['user_store']
    # result = user_store_collection.find ({'store_id': store_id})
    # result_list = list (result)
    session = getDatabaseSession()
    result = session.query(User_store).filter(User_store.store_id == store_id).all()
    if len (result) == 0:
        return False
    else:
        return True