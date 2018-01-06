import uuid
from datetime import datetime

from database import Database
from models.post import Post


class Blog(object):

    def __init__(self, author , title , description,author_id,  _id=None):
        self.author = author
        self.autho_id  = author_id
        self.title = title
        self.description =description
        self._id = uuid.uuid4().hex if _id is None else _id


    def new_post(self, title, content, date = datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title= title,
                    content=content,
                    author = self.author,
                    created_date = date)

        post.save_to_mongo()

    def get_posts(self):
         return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id' : self.author_id,
            'title' : self.title,
            'description' : self.description,
            '_id': self._id
        }
    @classmethod
    def get_from_mongo(cls,id):
        blog_data = Database.find_one(collection='blogs', query={'_id' :id})

        return cls(**blog_data)
    @staticmethod
    def from_blog(id):
        return Database.find(collection='posts', query={'blog_id': id})

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection= 'blogs' , query={'id': id})

        return cls(**blog_data)
    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query = {'auhtor_id' : author_id})
        return [cls(**blog) for blog in blogs]