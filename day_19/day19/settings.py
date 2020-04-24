import os

MONGOALCHEMY_DATABASE = os.environ.get('mongodb')
SECRET_KEY = os.environ.get('secret')
MONGO_CONNECTION_STRING = os.environ.get('MONGO_URI')