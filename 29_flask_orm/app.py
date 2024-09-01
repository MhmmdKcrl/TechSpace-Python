from flask import Flask

from datetime import timedelta

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:12345@localhost:3306/my_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = '6fa26729311dfe8d3aa2da958b5a0339'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)


from controllers import *
from extensions import *
from models import *

if __name__ == '__main__':
    app.run(debug=True)