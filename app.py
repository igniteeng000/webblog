from flask import Flask, render_template, request, session, make_response

from database import Database
from menu import Menu

#python flask mongo jinja
from models.blog import Blog
from models.user import User

app = Flask(__name__)
app.secret_key = "ashu"
# @app.route('/')
# def home_template():
#     return render_template('home.html')
#


@app.route('/')
def login_template():
    return render_template('login.html')

@app.route('/register')
def register_template():
    return render_template('register.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)


    else:
        session['email'] = None
    return render_template("profile.html", email = session['email'])

@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)
    session['email'] = email

    return render_template("profile.html", email = session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    user = User.get_blogs()
    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email = '')

@app.route('/blogs/new', methods=['POST','GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.emal, title, description, user._id)
        new_blog.save_to_mongo()
        return make_response(user_blogs(user._id))

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.get_posts()

    return render_template('posts.html', posts = blog.posts, blog_title=blog.title)
if __name__ == '__main__':
    app.run()
#Da tabase.initialize()
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