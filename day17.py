from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from day10 import emailcheck
import jwt
import os,uuid
import datetime as d
from functools import wraps

# Database directory
basedir = os.getcwd()

app_ = Flask(__name__)

#app config
"""
This config clause specifies the database location. And disabes an option to
track changes in database to False (it's turned on by default). Sqlite comes
by default with flask so no need to worry
about installing any rdbms
"""
app_.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,"app_.sqlite")  or os.getenv("DATABASE_URI")
app_.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_.config['SERET_KEY'] = os.getenv("SECRET_KEY") or input("Enter Secret key: ")

db = SQLAlchemy(app_)
ma = Marshmallow(app_)
bcrypt = Bcrypt(app_)

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
    #public_id = db.Column(db.String(50),unique=True)
    signup_date = db.Column(db.DateTime,default=d.datetime.utcnow())

# Auth Function/Decorator
def login_required(f):
    @wraps(f)
    def function(*args,**kwargs):
        token  = None
        if 'x-access-token' in request.headers:
            token = request.headers["x-access-token"]

            try:
                #try to fetch user data using token
                data = token.decode(token,app_.config["SECRET_KEY"])
                user = User.query.filter_by(email=data["email"]).first()

                if user:
                    return f(user,*args,**kwargs)
            except:
                return jsonify({'message': 'Token is invalid'}),401
        else:
            return make_response(jsonify({"message":"Token not found"})),404
    return function


# Signup Handler
@app_.route('/signup',methods=['POST'])
def signup():
    # fetch data
    user_data = request.get_json()
    # hash password
    password_hash = bcrypt.generate_password_hash(user_data["password"])
    # validate email using email checker from day10 (regex)
    if emailcheck(user_data["email"]):
        # checks to see if email doesn't already exists
        try:
            #new_user = User(password=password_hash,email=user_data["email"],public_id=str(uuid.uuid4()))
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

# Login/Auth Handler
@app_.route('/login')
def login():
    auth = request.authorization

    # check to see that payload is accurate
    if not auth or not auth.password or not auth.username:
        return make_response("Could not verify",401,{'WWW-Authenticate' : 'Basic realm="Login required"'})
    
    user = User.query.filter_by(username=auth.username).first()
    if not user:
       return make_response("No such user found",401,{'WWW-Authenticate' : 'Basic realm="Login required"'})

    # Verify user password
    if bcrypt.check_password_hash(user.password,auth.password):
        token = jwt.encode({'email':user.email, 'exp' : d.datetime.utcnow() + d.timedelta(minutes=30)}, app_.config['SERET_KEY'])

        return jsonify({"token" : token.decode('UTF-8')})

    return make_response("No such user found",401,{'WWW-Authenticate' : 'Basic realm="Login required"'})

@login_required
@app_.route("/getuser/<email>")
def getuser(email):\
    #find user with email
    user = User.query.filter_by(email=email).first()
    date = user.signup_date
    date_ = str(date)
    time = date_.split(' ')
    return jsonify({"username":user.username,"email":user.email,"date":str(date.strftime('%A')),"time":f"{time[1]} {date.strftime('%p')}"})

if __name__ == '__main__':
    app_.run(debug=True)


