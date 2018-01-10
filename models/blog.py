import uuid
from datetime import datetime

from database import Database
from models.post import Post


class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_blog(self, title, description):
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self.id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        post = Post(title=title,
                    content=content,
                    created_date=date)

        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }
    #
    # @classmethod
    # def get_from_mongo(cls, id):
    #     blog_data = Database.find_one(collection='blogs', query={'_id': id})
    #
    #     return cls(**blog_data)

    @staticmethod
    def from_blog(_id):
        return Database.find(collection='posts', query={'blog_id': id})

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs', query={'_id': id})

        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]
