
from database import Database
from models.blog import Blog


class Menu(object):
    def __init__(self):
        self.user = input("Enter your author name")
        self.user_blog = None
        if self._user_has_account():
            print("Welcome back {}".format(self.user))
        else:
            self._prompt_user_for_account()


    def _user_has_account(self):
        blog = Database.find_one('blogs',{'author': self.user})

        if blog is not None:
            self.user_blog = Blog.get_from_mongo(blog['id'])
            return True

        else:
            return False

    def _prompt_user_for_account(self):
        title = input("Enter blog title")
        description = input("Enter your Description")
        blog = Blog(author = self.user,
                    title = title,
                    description = description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        read_or_write = input("Do you want to read (R) or write (W) blogs")

        if read_or_write == 'R' or read_or_write == 'r':
            self._list_blogs()
            self._view_blogs()
            pass
        elif read_or_write == 'W' or read_or_write == 'w':
            self._prompt_write_post()
        else:
            print("Thank you for blogging")

    def _list_blogs(self):
        blogs = Database.find(collection='blogs', query={})

        for blog in blogs:
            print("Date: {}, title: {},Author: {}".format(blog['id'],blog['title'],blog['author']))

    def _view_blogs(self):
        blog_to_see = input("Enter the ID of the blog you'd like to read: ")
        blog = Blog.get_from_mongo(blog_to_see)
        posts = blog.get_posts()
        for post in posts:
            print("Date: {}, title: {}\n\n{}".format(post['created_date'], post['title'], post['content']))

    def _prompt_write_post(self):
        self.user_blog.new_post()


