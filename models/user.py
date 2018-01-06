import datetime from datetime
from flask import session

from database import Database
from models.blog import Blog


class User(object):
    def __init__(self, email, password, _id = None):
        self.email = email
        self.password = password
        pass
    @classmethod
    def get_by_email(cls,email):
        data = Database.find_one("users" , {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)
    @staticmethod
    def login_valid(self, email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod  #here cls = User since we are using same class function
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True

        else:
            return False

    @staticmethod
    def login(user_email):
        #login valid is alreday called
        session['email'] = user_email

    @staticmethod
    def logout():
        # login valid is alreday called
        session['email'] = None

    def json(self):
        return {
            "email" : self.email,
            "_id" : self._id,
            "password" : self.password
        }
    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        blog =Blog(author=self.email,
                   author_id= self._id,
                   title = title,
                   description = description)

        blog.save_to_mongo()
    @staticmethod
    def new_post( blog_id, title, content, date = datetime.utcnow()):
        blog =Blog.from_mongo(blog_id)
        blog.new_post(title = title,
                      content = content,
                      date = date
                       )

    def save_to_mongo(self):
        Database.insert("users", self.json())