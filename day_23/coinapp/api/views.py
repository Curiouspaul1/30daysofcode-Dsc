from . import api
from coinapp.models import User,Wallet
from coinapp import db
from coinapp.extensions import emailcheck
from flask import request,make_response,jsonify
from sqlalchemy.exc import IntegrityError
from functools import wraps
import jwt

@api.route('/createuser',methods=['POST'])
def creatuser():
    data = request.get_json()
    if emailcheck(data['email']):
        try:
            new_user = User(name=data['name'],email=data['email'],tel=data['tel'],password=data['password'],transactionPin=data['pin'])
        except IntegrityError as e:
            return jsonify({"message":"pre-existing entry found in database"}),401
            raise e
        db.session.add(new_user)
        user_wallet = Wallet()
        user_wallet.user = new_user
        db.session.add(user_wallet)
        db.session.commit()
    return jsonify({"message":"Registration successful"}),200
