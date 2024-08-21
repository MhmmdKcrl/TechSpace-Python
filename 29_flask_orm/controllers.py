from flask import url_for, redirect, render_template, request

from  app import app
from models import Blog

user_list = [
    {
        'name': "User1",
        'email': "user1@mail.com",
        'password': "123"
    },
    {
        'name': "User 2",
        'email': "user2@mail.com",
        'password': "1234"
    },
    {
        'name': "User 3",
        'email': "user3@mail.com",
        'password': "12345"
    },
]



@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/home-redirect/')
def home_redirect():
    return redirect(url_for('index'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email:
            for i in user_list:
                if email == i['email']:
                    if password == i['password']:
                        return redirect(url_for('profile', name=i['name']))   
                    else:
                        message = 'Password is incorrect'
                        # return redirect(url_for('login'))   
    context = {
        'message': message
    }      


    return render_template('login.html', **context)


@app.route('/register/', methods=['GET', 'POST' ])
def register():
    if request.method == 'POST':
        name = request.form['name_form_post']
        email = request.form.get('email')
        password = request.form.get('password')
        user = {}
        user['name'] = name
        user['email'] = email
        user['password'] = password
        user_list.append(user)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/profile/<name>', methods=['GET'])
def profile(name):
    return render_template('profile.html', name=name)


@app.route('/blogs/')
def blogs():
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)


@app.route('/blogs/<int:id>/')
def blog(id):
    blog = Blog.query.get(id)
    message = None
    if blog is None:
        message = "Blog not found"
    
    return render_template('blog_detail.html', blog=blog, message=message)