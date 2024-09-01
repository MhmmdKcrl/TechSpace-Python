from flask import url_for, redirect, render_template, request, flash, session
from sqlalchemy import or_
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required

from  app import app
from models import Blog, Author, User
from extensions import db
from forms import RegisterForm, LoginForm

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


# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     message = None
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         if email:
#             for i in user_list:
#                 if email == i['email']:
#                     if password == i['password']:
#                         return redirect(url_for('profile', name=i['name']))   
#                     else:
#                         message = 'Password is incorrect'
#                         # return redirect(url_for('login'))   
#     context = {
#         'message': message
#     }      


#     return render_template('login.html', **context)


# @app.route('/register/', methods=['GET', 'POST' ])
# def register():
#     if request.method == 'POST':
#         name = request.form['name_form_post']
#         email = request.form.get('email')
#         password = request.form.get('password')
#         user = {}
#         user['name'] = name
#         user['email'] = email
#         user['password'] = password
#         user_list.append(user)
#         return redirect(url_for('login'))
#     return render_template('register.html')


# @app.route('/profile/<name>', methods=['GET'])
# def profile(name):
#     return render_template('profile.html', name=name)


@app.route('/blogs/')
def blogs():
    user = session.get('name', None)
    # user = session['name']
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs,  user=user)


@app.route('/blogs/<int:id>/')
def blog(id):
    blog = Blog.query.get(id)
    message = None
    if blog is None:
        message = "Blog not found"
    
    return render_template('blog_detail.html', blog=blog, message=message)



@app.route('/authors/', methods=['GET'])
def authors():
    user = "orxan"
    session["name"] = user
    session.permanent = True
    authors = Author.query.all()
    q = request.args.get('q')
    if q:

        # authors = Author.query.filter_by(name=q, surname=q).all()
        authors = Author.query.filter(or_(Author.name.like(f"%{q}%"), Author.surname.like(f"%{q}%"), Author.email.like(f"%{q}%") )).order_by(Author.name.desc()).all()

    return render_template('authors.html', authors=authors, q=q, user=user)



@app.route('/update_author/<int:id>/', methods=['GET', 'POST'])
def update_author(id):
    author = Author.query.get(id)
    message = None

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')

        print(request.form, "-----------")

        Author.query.filter_by(id=id).update(dict(
            name=name,
            surname=surname,
            email=email,
            password=password)
        )

        # author.name = name
        # author.surname = surname
        # author.email = email
        # author.password = password

        db.session.commit()
        message = f"Author {author.id} updated successfully"

    return render_template('update.html', author=author, message=message)


@app.route('/delete_author/<int:id>/', methods=['GET', 'POST'])
def delete_author(id):
    author = Author.query.get(id)
    message = None
    if request.method == 'POST':
        author.delete()
        message = f"Author {author.id} deleted successfully"
    
    print(message, "-----------")
    
    return render_template('delete.html', message=message)


@app.route('/create_author/', methods=['GET', 'POST'])
def create_author():
    message = None
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')

        author = Author(name=name, surname=surname, email=email, password=password)
        author.save()
        message = f"Author {author.name} {author.surname} created successfully"

    return render_template('create.html', message=message)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    # if session.get('name'):
    #     session.pop('name')
    # session.pop('name', None)
    form = RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            # print(form.data , "----------")
            user = User(
                name = form.name.data,
                surname = form.surname.data,
                mail = form.mail.data,
                password = form.password.data,
            )
            user.save()
            flash("Qeydiyyat ugurla tamamlandi", 'success')
            return redirect(url_for("login"))
        
        flash("Error var", 'danger')
    
    return render_template('register.html', form=form)



@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            mail = form.mail.data
            user = User.query.filter_by(mail=mail).first()
            
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Daxil oldunuz", 'success')
                return redirect(url_for('profile'))
            
        flash("Mail ve ya sifre yanlisdir", 'danger')
                

    return render_template('login.html', form=form)


@app.route('/profile/')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)


@app.route('/logout/')
def logout():
    logout_user()
    flash("Sistemden ugurla cixis edildi", 'info')
    return redirect(url_for('login'))