from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(config_object='day18.settings'):
    app = Flask(__name__
    app.config.from_object(config_object)
    
    mongo.init_app(app)

    return app
