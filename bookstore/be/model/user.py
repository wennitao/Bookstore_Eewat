import jwt
import time
import logging
from typing import Tuple
# import sqlite3 as sqlite
# import pymongo
# import pymongo.errors
from be.model import error
# from be.model import db_conn
from be.model.database import getDatabaseSession, getDatabaseBase
# from be.model.collection import Collection

from sqlalchemy import Column, String, create_engine, Integer, Text, Date
import time
# from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Base = getDatabaseBase()

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded

Base = getDatabaseBase()

class User(Base):
    print ("init user")
    __tablename__ = "user"

    user_id = Column(Text, primary_key=True, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    balance = Column (Integer, nullable=False)
    token = Column (Text)
    terminal = Column (Text)

    token_lifetime: int = 3600  # 3600 second

    # def __init__(self):
    #     # db_conn.DBConn.__init__(self)
    #     self.userCollection = Collection("user").collection
    #     self.userCollection.create_index("user_id", unique=True)

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            # self.conn.execute(
            #     "INSERT into user(user_id, password, balance, token, terminal) "
            #     "VALUES (?, ?, ?, ?, ?);",
            #     (user_id, password, 0, token, terminal), )
            # self.conn.commit()
            
            # mongoDB example
            # self.userCollection.insert_one(
            #     {
            #         "user_id": user_id,
            #         "password": password,
            #         "balance": 0,
            #         "token": token,
            #         "terminal": terminal
            #     }
            # )
            session = getDatabaseSession()
            new_user = User (user_id = user_id, password = password, balance = 0, token = token, terminal = terminal)
            print (new_user)
            session.add (new_user)
            session.commit()

        except SQLAlchemyError as e:
            print (str (e))
            session.rollback()
            return error.error_exist_user_id(user_id)
        except BaseException as e:
            print (str (e))
            return 530, "{}".format(str(e))
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> Tuple[int, str]:
        # cursor = self.conn.execute("SELECT token from user where user_id=?", (user_id,))
        # row = cursor.fetchone()
        # result = self.userCollection.find ({'user_id': user_id})
        # result_list = list (result)
        session = getDatabaseSession()
        result = session.query (User).filter (User.user_id == user_id).all()
        if len (result) == 0:
            return error.error_authorization_fail()
        db_token = result[0].token
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> Tuple[int, str]:
        # cursor = self.conn.execute("SELECT password from user where user_id=?", (user_id,))
        # row = cursor.fetchone()
        # result = self.userCollection.find ({'user_id': user_id})
        session = getDatabaseSession()
        result = session.query (User).filter (User.user_id == user_id).all()
        if len (result) == 0:
            return error.error_authorization_fail()
        if password != result[0].password:
            return error.error_authorization_fail()

        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> Tuple[int, str, str]:
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            # cursor = self.conn.execute(
            #     "UPDATE user set token= ? , terminal = ? where user_id = ?",
            #     (token, terminal, user_id), )
            # update_result = self.userCollection.update_one (
            #     {"user_id": user_id},
            #     {"$set": {"token": token, "terminal": terminal}}
            # )
            session = getDatabaseSession()
            session.query (User).filter (User.user_id == user_id).update ({"token": token, "terminal": terminal})
            session.commit()
            # if update_result.matched_count == 0:
            #     return error.error_authorization_fail() + ("", )
        except SQLAlchemyError as e:
            session.rollback()
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> bool:
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            # cursor = self.conn.execute(
            #     "UPDATE user SET token = ?, terminal = ? WHERE user_id=?",
            #     (dummy_token, terminal, user_id), )
            # update_result = self.userCollection.update_one (
            #     {"user_id": user_id},
            #     {"$set": {"token": dummy_token, "terminal": terminal}}
            # )
            # if update_result.matched_count == 0:
            #     return error.error_authorization_fail()
            session = getDatabaseSession()
            session.query (User).filter (User.user_id == user_id).update ({"token": dummy_token, "terminal": terminal})
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> Tuple[int, str]:
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            # cursor = self.conn.execute("DELETE from user where user_id=?", (user_id,))
            # delete_result = self.userCollection.delete_one({"user_id": user_id})
            # if delete_result.deleted_count == 0:
            #     return error.error_authorization_fail()
            session = getDatabaseSession()
            session.query (User).filter (User.user_id == user_id).delete()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            print (str (e))
            return 530, "{}".format(str(e))
        return 200, "ok"

    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            # cursor = self.conn.execute(
            #     "UPDATE user set password = ?, token= ? , terminal = ? where user_id = ?",
            #     (new_password, token, terminal, user_id), )
            # update_result = self.userCollection.update_one (
            #     {"user_id": user_id},
            #     {"$set": {"password": new_password, "token": token, "terminal": terminal}}
            # )
            # if update_result.matched_count == 0:
            #     return error.error_authorization_fail()
            session = getDatabaseSession()
            session.query (User).filter (User.user_id == user_id).update ({"password": new_password, "token": token, "terminal": terminal})
            session.commit()
            
        except SQLAlchemyError as e:
            session.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

def getBalance (user_id: str) -> int:
    # userCollection = Collection("user").collection
    # result = userCollection.find ({'user_id': user_id})
    # result_list = list (result)
    # return result_list[0]['balance']
    session = getDatabaseSession()
    result = session.query (User).filter (User.user_id == user_id).all()
    return result[0].balance