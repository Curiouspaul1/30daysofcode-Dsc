from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from day10 import emailcheck
import os

# Database directory
basedir = os.getcwd()

app = Flask(__name__)

#app config
"""
This config clause specifies the database location. And disabes an option to
track changes in database to False (it's turned on by default)
"""
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,"app.sqlite")  or os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

# Database Model
class User(db.Model):
    """
        The user class represents an sql table. It's schema is outlined
        below, as with the aid of an ORM (Sqlalchemy) or more precisely
        flask-sqlalchemy (a wrapper built around the more generic sqlalchemy).
        This allows me to write native python objects that translate to (more or less)
        SQL tables.
    """
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    username = db.Column(db.String(50),unique=True)
    email = db.Column(db.String(100),unique=True)   ## The unique property on email, disallows duplicate emails
    password = db.Column(db.String(100))

@app.route('/signup',methods=['POST'])
def signup():
    # fetch data
    user_data = request.get_json()
    # hash password
    password_hash = bcrypt.generate_password_hash(user_data["password"])
    # validate email using email checker from day10 (regex)
    if emailcheck(user_data["email"]):
        # checks to see if email doesn't already exists
        try:
            new_user = User(password=password_hash,email=user_data["email"])
            db.session.add(new_user)
        except IntegrityError:
            return make_response("User with email already exists",406)
        # checks also to see if username doesnt already exist
        try:
            new_user.username = user_data["username"]
            db.session.commit()
        except IntegrityError:
            return make_response("User with username already exists",406)
    else:
        return make_response("Invalid Email",406)
   
    return make_response("registration successful",200)

@app.route('/login',methods=['POST'])
def login():
    login_data = request.get_json()
    # find user with username or email
    user = User.query.filter_by(username=login_data["username"]).first() or User.query.filter_by(email=login_data["email"])
    if user:
        # fetch passowrd from database then compare
        password_hash = user.password
        if bcrypt.check_password_hash(password_hash,login_data["password"]):
            return make_response("Signed in successfully", 200)
        else:
            return make_response("Wrong password",401)
    else:
        return make_response("No such user found",404)