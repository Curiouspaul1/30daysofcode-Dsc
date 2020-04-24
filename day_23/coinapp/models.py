from . import db,ma

class User(db.Model):
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100),unique=True)
    tel = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    transactionPin = db.Column(db.Integer())
    wallet = db.relationship('Wallet',backref='user',uselist=False)

class Wallet(db.Model):
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    amount = db.Column(db.Float,default=0.00)
    transactionLogs = db.Column(db.PickleType())
    User_id = db.Column(db.ForeignKey('user.id'))

