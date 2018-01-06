from flask import Flask, render_template, request, session

from database import Database
from menu import Menu

#python flask mongo jinja
from models.user import User

app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('login.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login.valid(email, password):
        User.login(email)

    return render_template("profile.html", email = session['email'])

if __name__ == '__main__':
    app.run()
#Database.initialize()
#menu = Menu()
#menu.run_menu()


# from models.blog import Blog
# from models.post import Post
#
#
# Database.initialize()
# post = Post(blog_id="001" ,
#             title="a hope",
#             content="sample",
#             author="raj"
#              )
#
# blog = Blog(author="ashu",
#             title ="python projects",
#             description ="terminal blog"
#             )
#
# blog.new_post()
#
# blog.save_to_mongo()
#
# from_database = Blog.get_from_mongo(blog.id)
#
# print(blog.get_posts())
# #
# # #post.save_to_mongo()
# # posts = Post.from_blog('001')
# # print(Post.from_blog('5a4df0f785901b1bfc491be1'))
# # for post in posts:
# #     print(post)