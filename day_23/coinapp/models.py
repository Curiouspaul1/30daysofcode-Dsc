from ..coinapp import db,ma

class User(db.Model):
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Wallet(db.Model):
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    amount = db.Column(db.Integer())
    transactionLogs = db.Column(db.PickleType())
    transactionPin = db.Column(db.Integer())
