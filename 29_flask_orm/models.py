from extensions import db

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

