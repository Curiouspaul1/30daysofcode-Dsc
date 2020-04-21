from flask import Blueprint,request,make_response,jsonify,current_app,json
from functools import wraps
from day18 import bcrypt,mongo
from day18.extensions import emailcheck
import jwt
import datetime as d

main = Blueprint('main',__name__)

User = mongo.db.users

# Auth Function/Decorator
def login_required(f):
    @wraps(f)
    def function(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if token:
                try:
                    data = jwt.decode(token,current_app.config['SECRET_KEY'])
                    if data:
                        user = User.find_one({'email':data['email']}) or User.find_one({'username':data['email']})
                        if user:
                            return f(user,*args,**kwargs)
                        return jsonify({"message":"No such user found"})
                    else:
                        return jsonify({"message":'Token is invalid'}),401
                except:
                    return make_response(jsonify({"message": 'Token is invalid'}),401)
            else:
                return make_response(jsonify({"message":"Token not found"})),404
        else:
            return make_response(jsonify({"message":"Token not found"})),404
    return function

@main.route('/signup',methods=['POST'])
def signup():
    user_collection = mongo.db.users
    # fetch data
    user_data = request.get_json()
    # hash password
    password_hash = bcrypt.generate_password_hash(user_data["password"])
    # validate email using email checker from day10 (regex)
    if emailcheck(user_data["email"]):
        new_user = user_collection.insert({'username':user_data["username"],'password':password_hash,'email':user_data['email'],'signup_date':d.datetime.utcnow()})
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
    
    user = User.find_one({'email':auth['username']}) or User.find_one({'username':auth['username']})
    if not user:
       return make_response("No such user found",401,{'WWW-Authenticate' : 'Basic realm="Login required"'})

    # Verify user password
    if bcrypt.check_password_hash(user['password'],auth.password):
        token = jwt.encode({'email':user['email'], 'exp' : d.datetime.utcnow() + d.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])

        return jsonify({"token" : token.decode('UTF-8')})

    return make_response("No such user found",401,{'WWW-Authenticate' : 'Basic realm="Login required"'})


@login_required
@main.route("/getuser/<email>")
def getuser(email):
    #find user with email
    user = mongo.db.users
    result = user.find_one({'email':f'{email}'})
    date = result['signup_date']
    date_ = str(date)
    time = date_.split(' ')
    print(date)
    if result:
        return jsonify({"_id":str(result['_id']),"username":result['username'],"email":result['email'],"date":str(date).split(' ')[0],"time":f"{time[1]} ".split('.')[0] + f" {date.strftime('%p')}"})
    return jsonify({"message":"No such user found"})