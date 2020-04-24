from flask import Blueprint,request,make_response,jsonify,current_app,json
from functools import wraps
from day19 import bcrypt,mongo
from day19.extensions import emailcheck
from jwt.exceptions import ExpiredSignatureError
import jwt
import datetime as d

main = Blueprint('main',__name__)

# Mongo Data Schema/Model
class User(mongo.Document):
    """
    Flask-MongoAlchemy ODM mapper class,
    that models users in the application. Mongoose
    isn't available in flask so MongoAlchemy is the next 
    best option - it does basically the same thing
    """
    id = mongo.ObjectIdField().gen()
    username = mongo.StringField()
    email = mongo.StringField()
    password = mongo.BinaryField()
    signup_date = mongo.DateTimeField()

# Auth Function/Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

            if token:
                try:
                    data = jwt.decode(token,current_app.config['SECRET_KEY'])
                    active_user = User.query.filter(User.email==data['email']).first() or User.query.filter(User.username==data['email']).first()
                except ExpiredSignatureError as e:
                    return jsonify({"message":"Token is expired"}),401
                    raise e
                
                return f(active_user, *args, **kwargs)
            else:
                return jsonify({'message':'Token is missing'}),404
        else:
            return jsonify({'message':'Token header is missing'}),404
    return decorated

@main.route('/createuser',methods=['POST'])
def signup():
    #user_collection = mongo.db.users
    # fetch data
    user_data = request.get_json()
    # hash password
    password_hash = bcrypt.generate_password_hash(user_data["password"])
    # validate email using email checker from day10 (regex)
    if emailcheck(user_data["email"]):
        #new_user = user_collection.insert({'username':user_data["username"],'password':password_hash,'email':user_data['email'],'signup_date':d.datetime.utcnow()})
        new_user = User(username=user_data['username'],password = password_hash,email = user_data['email'],signup_date=d.datetime.utcnow())
        new_user.save()
    else:
        return make_response("Invalid Email",406)
   
    return make_response("registration successful",200)

# Login/Auth Handler
@main.route('/login')
def login():
    auth = request.authorization

    # check to see that payload is accurate
    if not auth or not auth.password or not auth.username:
        return make_response("Could not verify",401,{'WWW-Authenticate' : 'Basic realm="Login required"'})
    
    user = User.query.filter(User.email == auth['username']).first() or User.query.filter(User.username == auth['username']).first()
    if not user:
       return make_response("No such user found",401,{'WWW-Authenticate' : 'Basic realm="Login required"'})

    # Verify user password
    if bcrypt.check_password_hash(user.password,auth.password):
        token = jwt.encode({'email':user.email, 'exp' : d.datetime.utcnow() + d.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
        return jsonify({"token" : token.decode('UTF-8')})

    return make_response("Incorrect Password",401,{'WWW-Authenticate' : 'Basic realm="Login required"'})



@main.route("/getuser/<email>")
@token_required
def getuser(active_user,email):
    #find user with email
    result = User.query.filter(User.email == f'{email}').first()
    date = result.signup_date
    date_ = str(date)
    time = date_.split(' ')
    print(date)
    if result:
        return jsonify({"_id":str(result.id),"username":result.username,"email":result.email,"date":str(date).split(' ')[0],"time":f"{time[1]} ".split('.')[0] + f" {date.strftime('%p')}"})
    return jsonify({"message":"No such user found"})

@main.route('/getusers')
@token_required
def getusers(active_user):
    users = User.query.all()
    result = []
    for user in users:
        date = user.signup_date
        date_ = str(date)
        time = date_.split(' ')
        result.append({"_id":str(user.id),"username":user.username,"email":user.email,"date":str(date).split(' ')[0],"time":f"{time[1]} ".split('.')[0] + f" {date.strftime('%p')}"})
    return jsonify({"users":result})


@main.route('/delete_user/<username>',methods=['DELETE'])
@token_required
def delete_user(active_user,username):
    # fetch user
    user = User.query.filter(User.username == f'{username}').first()
    if user:
        user.remove()
        return jsonify({"message":"Deleted successfully"}),200
    return jsonify({"message":"No such user found"}),404

@main.route('/update_user/<username>',methods=['PUT'])
@token_required
def update_user(active_user,username):
    user = User.query.filter(User.username == f'{username}').first()
    email = request.json['email']
    if user:
        if emailcheck(email):
            user.email = email
            user.save()
        else:
            return jsonify({"message":"Invalid entry"}),401
    else:
        return jsonify({"message":"User not found"}),404
    return jsonify({"message":"Updated user successfully"}),200

