import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(),'coinapp.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = os.getenv('secret')

config = {
    "default":Config
}