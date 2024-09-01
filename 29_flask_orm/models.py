from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from flask_security import RoleMixin

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, default="default_blog.jpg")
    is_active = db.Column(db.Boolean, default=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), )
    authors = db.relationship('Author', backref=db.backref('blogs', uselist = True, cascade="all, delete-orphan"))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f"<{self.title}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
    

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, default="default.jpg")


    def __repr__(self):
        return f"<{self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<{self.name}>"


student_course = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)

    role_id = db.relationship('Role', secondary = 'user_roles')


    def __repr__(self):
        return f"<{self.name}>"
    
    @property
    def full_name(self):
        return f"{self.name} {self.surname}"
    

    def __init__(self, name, surname, mail, password):
        self.name = name
        self.surname = surname
        self.mail = mail
        self.password = generate_password_hash(password)
    

    def save(self):
        db.session.add(self)
        db.session.commit()




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
