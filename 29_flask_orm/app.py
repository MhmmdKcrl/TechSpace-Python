from flask import Flask


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:12345@localhost:3306/my_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


from controllers import *
from extensions import *
from models import *

if __name__ == '__main__':
    app.run(debug=True)